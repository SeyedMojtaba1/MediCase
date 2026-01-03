from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from drf_spectacular.utils import extend_schema
from .serializer import (
    ScenarioCreateSerializer, 
    ScenarioRetrieveSerializer, 
    feedbackCreateSerializer, 
    StudentLogSerializer, 
    FeedbackRetrieveSerializer,
    ScenarioListSerializer,
    FeedbackListSerializer,
    StudentScenarioRankSerializer,
    SectionLeaderboardSerializer,
)
from .models import PulmonologyScenario, PulmonologyFeedback
from django.contrib.auth import get_user_model
from .utils import senario_creator_celery, feedback_creator_celery, decode_short_uuid
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from rest_framework.views import APIView
from django.db.models import Max, F, FloatField
from django.db.models.functions import Cast
from classroom.models import StudentSection
import secrets
import string

User = get_user_model()

ALPHABET = string.ascii_uppercase + string.digits

def generate_tracking_code(length: int = 10) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

@extend_schema(
    responses=ScenarioCreateSerializer
)
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def scenario_create(request):
    user = request.user
    
    try:
        user = User.objects.get(personal_number=user.personal_number)
    except User.DoesNotExist:
        return Response(
            {"detail": "User is not exist."}
        )
    
    if user.scenario_credit <= 0:
        return Response(
            {"detail": "User Have not enough credit."}
        )
    
    tracking_code = generate_tracking_code(10)
    senario_creator_celery.delay(user.personal_number, tracking_code)

    return Response({"tracking_code": tracking_code}, status=status.HTTP_200_OK)

class ScenarioRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioRetrieveSerializer
    queryset = PulmonologyScenario.objects.all()
    lookup_field = 'tracking_code'
    lookup_value_regex = '[^/]+'
    
class ScenarioListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioListSerializer

    def get_queryset(self):
        personal_num = self.kwargs.get('personal_number')
        
        return PulmonologyScenario.objects.filter(user__personal_number=personal_num)

@extend_schema(
    request=StudentLogSerializer,
    responses=feedbackCreateSerializer
)
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def feedback_create(request, *args, **kwargs):
    user = request.user
    scenario_tracking_code = request.parser_context['kwargs'].get('scenario_tracking_code')
    serializer = StudentLogSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    student_log = serializer.data['student_log']
    
    try:
        user = User.objects.get(personal_number=user.personal_number)
    except User.DoesNotExist:
        return Response(
            {"detail": "User is not exist."}
        )
        
    try:
        pulmonology_scenario = PulmonologyScenario.objects.get(tracking_code=scenario_tracking_code)
    except PulmonologyScenario.DoesNotExist:
        return Response(
            {"detail": "Scenario is not exist."}
        )
    
    disease = pulmonology_scenario.disease.english_name
    disease_type = pulmonology_scenario.disease.type_disease
    
    feedback_tracking_code = generate_tracking_code(10)
    feedback_creator_celery.delay(feedback_tracking_code, scenario_tracking_code, disease, disease_type, student_log)

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
        personal_num = self.kwargs.get('personal_number')
        
        return PulmonologyFeedback.objects.filter(scenario__user__personal_number=personal_num)

class StudentRankingPagination(PageNumberPagination):
    page_size = 10  # تعداد دانشجو در هر صفحه
    page_size_query_param = 'page_size'  # کلاینت می‌تواند با این پارامتر تعداد را تغییر دهد
    max_page_size = 100

class StudentRankingListView(generics.ListAPIView):
    serializer_class = StudentScenarioRankSerializer
    pagination_class = StudentRankingPagination  # <--- این خط اضافه شد
    
    def get_queryset(self):
        return User.objects.annotate(
            completed_scenarios_count=Count(
                'userPulmonologyScenario', 
                filter=Q(userPulmonologyScenario__done=True)
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

        # 1. استخراج شماره پرسنلی دانشجویان فعال در کلاس (استفاده از مدل StudentSection اپلیکیشن classroom)
        active_student_numbers = StudentSection.objects.filter(
            section_id=section_uuid,
            student_status='Active'
        ).values_list('student__personal_number', flat=True)

        # 2. اصلاح مسیر Join در متد Max با استفاده از related_name صحیح
        return User.objects.filter(personal_number__in=active_student_numbers).annotate(
            top_score=Max(
                Cast(
                    # مسیر صحیح: کاربر -> سناریوها -> فیدبک‌ها (با related_name درست) -> فیلد JSON
                    F('userPulmonologyScenario__feedbackpulmonologyscenario__feedback__score__obtained'),
                    FloatField()
                ),
                # فیلتر برای اطمینان از اینکه فقط فیدبک‌های نهایی شده محاسبه شوند
                filter=Q(userPulmonologyScenario__feedbackpulmonologyscenario__generated=True)
            )
        ).exclude(top_score=None).order_by('-top_score')
        
class StudentRankInSectionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, section_id): # پارامترها را از URL دریافت می‌کند
        student = self.request.user
        try:
            section_uuid = decode_short_uuid(section_id)
        except ValueError:
            return Response(
                {"message": "شناسه کلاس (section ID) نامعتبر است."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # ۱. ایجاد لیدربورد کلاس بر اساس شماره پرسنلی دانشجویان فعال
        leaderboard = User.objects.filter(
            studentsections__section_id=section_uuid,
            studentsections__student_status='Active'
        ).annotate(
            score=Max(
                Cast(
                    F('userPulmonologyScenario__feedbackpulmonologyscenario__feedback__score__obtained'), 
                    FloatField()
                )
            )
        ).exclude(score=None).order_by('-score')

        # ۲. پیدا کردن رتبه دانشجو با مقایسه personal_number
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
        # ۱. پیدا کردن فیدبک و بررسی مالکیت آن
        try:
            # استفاده از select_related برای واکشی بهینه اطلاعات سناریو و کاربر
            target_feedback = PulmonologyFeedback.objects.select_related(
                'scenario__user'
            ).get(tracking_code=tracking_code)
        except PulmonologyFeedback.DoesNotExist:
            return Response({"error": "فیدبک یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        # ۲. چک کردن اینکه درخواست‌دهنده همان مالک فیدبک باشد
        # در مدل کاربر شما کلید اصلی user_id است
        if target_feedback.scenario.user.user_id != request.user.user_id:
            return Response(
                {"error": "شما اجازه دسترسی به رتبه این فیدبک را ندارید."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        student = target_feedback.scenario.user
        
        # ۳. پیدا کردن کلاس (Section) فعال دانشجو
        student_section = StudentSection.objects.filter(
            student=student, 
            student_status='Active'
        ).first()

        if not student_section:
            return Response({"error": "کلاس فعالی برای شما یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        section_uuid = student_section.section_id

        # ۴. ایجاد لیدربورد کلاس بر اساس بالاترین نمره دانشجویان
        leaderboard = User.objects.filter(
            studentsections__section_id=section_uuid,
            studentsections__student_status='Active'
        ).annotate(
            best_score=Max(
                Cast(
                    F('userPulmonologyScenario__feedbackpulmonologyscenario__feedback__score__obtained'), 
                    FloatField()
                ),
                filter=Q(userPulmonologyScenario__feedbackpulmonologyscenario__generated=True)
            )
        ).exclude(best_score=None).order_by('-best_score')

        # ۵. پیدا کردن رتبه دانشجو در لیدربورد
        rank = None
        for index, user in enumerate(leaderboard):
            if user.personal_number == student.personal_number:
                rank = index + 1
                break

        return Response({
            "tracking_code": tracking_code,
            "rank_in_section": rank,
            "total_students": leaderboard.count(),
            "your_obtained_score": target_feedback.feedback.get('score', {}).get('obtained'),
            "section_name": student_section.section.name
        })

class SectionLeaderboardBySectionIdView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionLeaderboardSerializer

    def get_queryset(self):
        # دریافت شناسه کلاس از URL
        short_id = self.kwargs.get('section_id')
        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            return User.objects.none()

        # بررسی امنیتی: آیا کاربر درخواست‌دهنده عضو فعال این کلاس هست؟
        is_member = StudentSection.objects.filter(
            section_id=section_uuid,
            student=self.request.user,
            student_status='Active'
        ).exists()

        if not is_member:
            # اگر کاربر عضو کلاس نباشد، لیست خالی برمی‌گردد (عدم دسترسی)
            return User.objects.none()

        # ۱. استخراج لیست شماره پرسنلی تمام دانشجویان فعال در این کلاس
        active_student_numbers = StudentSection.objects.filter(
            section_id=section_uuid,
            student_status='Active'
        ).values_list('student__personal_number', flat=True)

        # ۲. رتبه‌بندی تمام دانشجویان کلاس بر اساس بالاترین امتیاز کسب شده
        return User.objects.filter(personal_number__in=active_student_numbers).annotate(
            top_score=Max(
                Cast(
                    F('userPulmonologyScenario__feedbackpulmonologyscenario__feedback__score__obtained'),
                    FloatField()
                ),
                filter=Q(userPulmonologyScenario__feedbackpulmonologyscenario__generated=True)
            )
        ).exclude(top_score=None).order_by('-top_score')