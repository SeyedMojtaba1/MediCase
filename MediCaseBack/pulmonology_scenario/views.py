from rest_framework import viewsets, generics, permissions, status, decorators
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializer import (
    UserScenarioAttemptListSerializer, 
    ScenarioRetrieveSerializer, 
    feedbackCreateSerializer, 
    StudentLogSerializer, 
    FeedbackRetrieveSerializer,
    FeedbackListSerializer,
    StudentScenarioRankSerializer,
    SectionLeaderboardSerializer,
    RankingOutputSerializer,
    RankingInputSerializer,
)
from django.db.models import Sum, Q
from django.utils import timezone
from .models import ScenarioTemplate, StudentLog, PulmonologyFeedback, UserScenarioAttempt, PulmonologyFeedback, DailyScenario
from classroom.models import Section
from django.contrib.auth import get_user_model
from .utils import senario_creator_celery, feedback_creator_celery, decode_short_uuid
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from rest_framework.views import APIView
from django.db.models import Max, F, FloatField
from django.db.models.functions import Cast
from classroom.models import StudentSection
from django.db import transaction
import secrets
import random
import string

User = get_user_model()

ALPHABET = string.ascii_uppercase + string.digits

def generate_tracking_code(length: int = 10) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

@extend_schema(
    responses={200: "Tracking Code JSON"}
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def scenario_create(request):
    user = request.user
    
    with transaction.atomic():
        user_obj = User.objects.select_for_update().get(pk=user.pk)
        
        if user_obj.scenario_credit <= 0:
            return Response(
                {"detail": "اعتبار شما برای ساخت سناریو کافی نیست."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user_obj.scenario_credit -= 1
        user_obj.save()

        unattempted_template = ScenarioTemplate.objects.exclude(
            attempts__user=user_obj
        ).first() 

        if unattempted_template:
            tracking_code = unattempted_template.tracking_code
            
            UserScenarioAttempt.objects.create(
                user=user_obj,
                scenario_template=unattempted_template,
                is_done=False
            )
            
            message = "سناریو از مخزن موجود با موفقیت به شما اختصاص یافت."
        
        else:
            tracking_code = generate_tracking_code(10)
            senario_creator_celery.delay(user_obj.personal_number, tracking_code)
            message = "سناریوهای موجود تمام شده بود. درخواست ساخت سناریو جدید با هوش مصنوعی ثبت شد."

    return Response(
        {
            "message": message,
            "tracking_code": tracking_code,
            "remaining_credit": user_obj.scenario_credit
        }, 
        status=status.HTTP_200_OK
    )

class ScenarioRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioRetrieveSerializer
    queryset = ScenarioTemplate.objects.all()
    lookup_field = 'tracking_code'
    lookup_value_regex = '[^/]+'
    
class ScenarioListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserScenarioAttemptListSerializer 

    def get_queryset(self):
        return UserScenarioAttempt.objects.filter(
            user=self.request.user
        ).select_related('scenario_template')

@extend_schema(
    request=StudentLogSerializer,
    responses={200: "Tracking Code JSON"}
)
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def feedback_create(request, *args, **kwargs):
    user = request.user
    scenario_tracking_code = kwargs.get('scenario_tracking_code')
    
    serializer = StudentLogSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    student_log_data = serializer.validated_data['student_log']
    
    try:
        template = ScenarioTemplate.objects.get(tracking_code=scenario_tracking_code)
    except ScenarioTemplate.DoesNotExist:
        return Response({"detail": "سناریو یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    # پیدا کردن آخرین تلاش کاربر در صورت وجود
    attempt = UserScenarioAttempt.objects.filter(
        user=user, 
        scenario_template=template
    ).order_by('-start_time').first()

    with transaction.atomic():
        # اگر تلاشی از قبل وجود نداشت، همین الان یکی می‌سازیم
        if not attempt:
            attempt = UserScenarioAttempt.objects.create(
                user=user,
                scenario_template=template,
                is_done=True
            )
        # اگر وجود داشت (مثلا از طریق سناریوی روزانه) وضعیت آن را به اتمام‌یافته تغییر می‌دهیم
        elif not attempt.is_done:
            attempt.is_done = True
            attempt.save()

        # ثبت لاگ
        StudentLog.objects.create(
            attempt=attempt,
            action_log=student_log_data
        )

        disease_name = template.disease.english_name if template.disease else "Unknown"
        disease_type = template.disease.type_disease if template.disease else "Unknown"
        feedback_tracking_code = generate_tracking_code(10)
        
        # ارسال به Celery برای پردازش هوش مصنوعی
        feedback_creator_celery.delay(
            feedback_tracking_code, 
            str(attempt.attempt_id),
            disease_name, 
            disease_type, 
            student_log_data
        )
        
    return Response({"tracking_code": feedback_tracking_code}, status=status.HTTP_200_OK)

class FeedbackRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackRetrieveSerializer
    queryset = PulmonologyFeedback.objects.all()
    lookup_field = 'tracking_code' 
    lookup_value_regex = '[^/]+'

class FeedbackListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackListSerializer

    def get_queryset(self):
        return PulmonologyFeedback.objects.filter(
            attempt__user=self.request.user
        ).select_related('attempt', 'attempt__scenario_template')

class StudentRankingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class StudentRankingListView(generics.ListAPIView):
    serializer_class = StudentScenarioRankSerializer
    pagination_class = StudentRankingPagination
    
    def get_queryset(self):
        return User.objects.annotate(
            completed_scenarios_count=Count(
                'attempts', 
                filter=Q(attempts__is_done=True)
            )
        ).order_by('-completed_scenarios_count')
        
class SectionLeaderboardView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionLeaderboardSerializer
    lookup_field = "section_id"

    def get_queryset(self):
        short_id = self.kwargs.get('section_id')
        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            return User.objects.none()

        active_student_numbers = StudentSection.objects.filter(
            section_id=section_uuid,
            student_status='Active'
        ).values_list('student__personal_number', flat=True)

        # اصلاح کوئری: استفاده از attempts__score به جای مسیر پیچیده JSON
        return User.objects.filter(personal_number__in=active_student_numbers).annotate(
            top_score=Max('attempts__score', filter=Q(attempts__is_done=True))
        ).exclude(top_score=None).order_by('-top_score')
        
class StudentRankInSectionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, section_id):
        student = self.request.user
        try:
            section_uuid = decode_short_uuid(section_id)
        except ValueError:
            return Response({"message": "Invalid section ID"}, status=400)
            
        # اصلاح کوئری لیدربرد
        leaderboard = User.objects.filter(
            studentsections__section_id=section_uuid,
            studentsections__student_status='Active'
        ).annotate(
            score=Max('attempts__score', filter=Q(attempts__is_done=True))
        ).exclude(score=None).order_by('-score')

        rank = None
        student_score = 0
        
        for index, user in enumerate(leaderboard):
            if user.personal_number == student.personal_number:
                rank = index + 1
                student_score = user.score
                break
        
        if rank is None:
            return Response({"error": "امتیازی برای شما در این کلاس یافت نشد."}, status=404)

        return Response({
            "personal_number": student.personal_number,
            "rank": rank,
            "total_students": leaderboard.count(),
            "best_score": student_score
        })
        
class FeedbackRankInSectionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "tracking_code"
    
    def get(self, request):
        tracking_code = self.kwargs.get('tracking_code')
        try:
            # اینجا مسیر scenario__user تغییر کرده است
            # فیدبک -> attempt -> user
            target_feedback = PulmonologyFeedback.objects.select_related(
                'attempt__user'
            ).get(tracking_code=tracking_code)
        except PulmonologyFeedback.DoesNotExist:
            return Response({"error": "فیدبک یافت نشد."}, status=404)

        if target_feedback.attempt.user.user_id != request.user.user_id:
            return Response({"error": "Forbidden"}, status=403)

        student = target_feedback.attempt.user
        student_section = StudentSection.objects.filter(
            student=student, 
            student_status='Active'
        ).first()

        if not student_section:
            return Response({"error": "کلاس فعالی برای شما یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        section_uuid = student_section.section_id

        leaderboard = User.objects.filter(
            studentsections__section_id=section_uuid,
            studentsections__student_status='Active'
        ).annotate(
            best_score=Max('attempts__score', filter=Q(attempts__is_done=True))
        ).exclude(best_score=None).order_by('-best_score')

        rank = None
        for index, user in enumerate(leaderboard):
            if user.personal_number == student.personal_number:
                rank = index + 1
                break

        return Response({
            "tracking_code": tracking_code,
            "rank_in_section": rank,
            "total_students": leaderboard.count(),
            "your_obtained_score": target_feedback.attempt.score, 
            "section_name": student_section.section.name
        })

class SectionLeaderboardBySectionIdView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionLeaderboardSerializer
    lookup_field = "section_id"
    
    def get_queryset(self):
        short_id = self.kwargs.get('section_id')
        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            return User.objects.none()

        is_member = StudentSection.objects.filter(
            section_id=section_uuid,
            student=self.request.user,
            student_status='Active'
        ).exists()

        if not is_member:
            return User.objects.none()

        active_student_numbers = StudentSection.objects.filter(
            section_id=section_uuid,
            student_status='Active'
        ).values_list('student__personal_number', flat=True)

        return User.objects.filter(personal_number__in=active_student_numbers).annotate(
            top_score=Max(
                Cast(
                    F('userPulmonologyScenario__feedbackpulmonologyscenario__feedback__score__obtained'),
                    FloatField()
                ),
                filter=Q(userPulmonologyScenario__feedbackpulmonologyscenario__generated=True)
            )
        ).exclude(top_score=None).order_by('-top_score')

class GetDailyScenarioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # 1. گرفتن لیست ID تمام سناریوهای تولید شده برای امروز
        # (Referring to DailyScenario model structure in models.py)
        today_daily_ids = DailyScenario.objects.filter(date=today).values_list('scenario_template_id', flat=True)
        
        if not today_daily_ids:
            return Response(
                {"detail": "سناریوهای روزانه برای امروز هنوز تولید نشده‌اند."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. بررسی اینکه آیا کاربر قبلاً در این روز تلاشی برای سناریوهای روزانه داشته است؟
        # ما چک می‌کنیم آیا کاربر برای هیچ‌یک از IDهای سناریوهای امروز، رکوردی در UserScenarioAttempt دارد یا خیر.
        # (Referring to UserScenarioAttempt model structure in models.py)
        has_attempted_today = UserScenarioAttempt.objects.filter(
            user=user,
            scenario_template__template_id__in=today_daily_ids
        ).exists()

        if has_attempted_today:
            return Response(
                {"detail": "شما سهمیه سناریوی روزانه امروز خود را استفاده کرده‌اید."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. انتخاب تصادفی یک سناریو از لیست امروز
        selected_template_id = random.choice(list(today_daily_ids))
        selected_template = ScenarioTemplate.objects.get(template_id=selected_template_id)

        # 4. ثبت شروع سناریو (ایجاد Attempt)
        # به محض اینکه کاربر درخواست داد، این رکورد ساخته می‌شود تا کاربر نتواند دوباره درخواست دهد (حتی اگر سناریو را تمام نکند)
        attempt = UserScenarioAttempt.objects.create(
            user=user,
            scenario_template=selected_template,
            is_done=False
        )

        # 5. بازگرداندن اطلاعات سناریو
        response_data = {
            "attempt_id": attempt.attempt_id,
            "title": selected_template.title,
            "scenario_data": selected_template.content, # (ScenarioTemplate content field)
            "tracking_code": selected_template.tracking_code,
            "message": "سناریوی روزانه شما با موفقیت ایجاد شد."
        }

        return Response(response_data, status=status.HTTP_200_OK)

class DailyScenarioRankingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        # دریافت تلاش‌های موفق سناریوهای امروز
        attempts = UserScenarioAttempt.objects.filter(
            scenario_template__daily_instances__date=today,
            is_done=True,
            score__isnull=False
        ).select_related('user', 'scenario_template').order_by('-score', 'end_time')

        ranking_data = []
        
        for rank, attempt in enumerate(attempts, start=1):
            user = attempt.user
            
            # ساخت آدرس عکس پروفایل
            profile_image_url = None
            if user.profile_image:
                try:
                    profile_image_url = request.build_absolute_uri(user.profile_image.url)
                except:
                    profile_image_url = None

            ranking_data.append({
                "rank": rank,
                "username": user.username,
                "profile_image": profile_image_url,
                "score": attempt.score,
                "finished_at": attempt.end_time
            })

        return Response(ranking_data, status=status.HTTP_200_OK)
    
class AdvancedUniversityRankingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[RankingInputSerializer],
        responses={200: RankingOutputSerializer(many=True)} 
    )
    def get(self, request):
        user = request.user
        
        input_serializer = RankingInputSerializer(data=request.query_params)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        validated_data = input_serializer.validated_data
        short_section_id = validated_data.get('section_id')
        filter_date = validated_data.get('date')
        filter_subject = validated_data.get('subject')

        users_queryset = User.objects.all()

        if not (user.main_role and user.main_role.name.lower() == 'superadmin'):
            if user.university:
                users_queryset = users_queryset.filter(university=user.university)
            else:
                return Response({"message": "شما به دانشگاهی متصل نیستید."}, status=status.HTTP_403_FORBIDDEN)

        attempt_filters = Q(attempts__is_done=True) & Q(attempts__score__isnull=False)

        if short_section_id:
            try:
                section_uuid = decode_short_uuid(short_section_id)
                section = Section.objects.get(section_id=section_uuid)
                
                if user.main_role.name.lower() != 'superadmin' and section.teacher and section.teacher.university != user.university:
                     return Response({"message": "شما به این کلاس دسترسی ندارید."}, status=status.HTTP_403_FORBIDDEN)

                users_queryset = users_queryset.filter(
                    studentsections__section=section,
                    studentsections__student_status='Active'
                )
                
                if section.subject:
                    attempt_filters &= Q(attempts__scenario_template__related_subject=section.subject)
                    
            except (ValueError, Section.DoesNotExist):
                return Response({"message": "کلاس مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        if filter_date:
            attempt_filters &= Q(attempts__end_time__date=filter_date)

        if filter_subject:
            attempt_filters &= Q(attempts__scenario_template__related_subject__english_name__iexact=filter_subject)

        leaderboard = users_queryset.annotate(
            total_score=Sum('attempts__score', filter=attempt_filters)
        ).filter(
            total_score__isnull=False,
            total_score__gt=0
        ).order_by('-total_score')

        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(leaderboard, request)

        start_rank = paginator.page.start_index() if result_page else 1
        
        for index, user_obj in enumerate(result_page):
            user_obj.rank = start_rank + index
            user_obj.score = user_obj.total_score 

        serializer = RankingOutputSerializer(result_page, many=True, context={'request': request})

        return paginator.get_paginated_response(serializer.data)