from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.response import Response
from .serializer import (
    SectionListSerializer,
    SectionRetrieveSerializer, 
    SectionUpdateSerializer,
    SectionCreateSerializer,
    SetSectionImageSerializer,
    StudentSectionSerializer,
    StudentSectionRetrieveSerializer,
    StudentSectionRemoveSerializer,
    StudentSectionListSerializer,
    MembersSectionSerializer,
    SemesterSerializer, 
    SubjectSerializer, 
    StudentSubjectSerializer,
    StudentSubjectListSerializer,
    StudentSubjectRetrieveSerializer,
    HospitalSerializer,
    HospitalSubjectSerializer,
    HospitalSubjectListSerializer,
    HospitalSubjectRetrieveSerializer,
)
from .models import Section, StudentSection, Semester, Subject, StudentSubject, Hospital, HospitalSubject
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from django.contrib.auth import get_user_model
from .utils import decode_short_uuid

User = get_user_model()

class SectionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionListSerializer
    queryset = Section.objects.all()
    
    def list(self, request, *args, **kwargs):
        user = self.request.user

        if not user.main_role:
            queryset = self.get_queryset().none()

        role = user.main_role.name.lower()

        if role == "superadmin":
            queryset = self.get_queryset()
        elif role == "teacher":
            queryset = self.get_queryset().filter(teacher=user)
        elif role == "student":
            queryset = self.get_queryset().filter(sectionstudents__student=user)
        else:
            queryset = self.get_queryset().none()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SectionRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionRetrieveSerializer
    queryset = Section.objects.all()
    lookup_field = 'section_id'
    lookup_value_regex = '[^/]+'
    
    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        short_id = self.kwargs.get(self.lookup_field)
        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            return Response(
                {"message": "شناسه کلاس (section ID) نامعتبر است."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.main_role:
            return Response({"message": "Section is not exist."}, status=status.HTTP_400_BAD_REQUEST)

        role = user.main_role.name.lower()

        if role == "superadmin":
            queryset = self.get_queryset(section_id=section_uuid).first()
        elif role == "teacher":
            queryset = self.get_queryset().filter(teacher=user, section_id=section_uuid).first()
        elif role == "student":
            queryset = self.get_queryset().filter(sectionstudents__student=user, section_id=section_uuid).first()
        else:
            return Response({"message": "Section is not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

class SectionUpdateViewSet(viewsets.ModelViewSet):
    http_method_names = ['put']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionUpdateSerializer
    queryset = Section.objects.all() 
    lookup_field = 'section_id'
    
    def put(self, request, *args, **kwargs):
        user = request.user
        short_id = self.kwargs.get(self.lookup_field)

        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            return Response(
                {"message": "شناسه کلاس (section ID) نامعتبر است."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            section = Section.objects.get(section_id=section_uuid)
        except Section.DoesNotExist:
            return Response({"message": "کلاسی با این نام وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        if not user.main_role:
             return Response({"message": "نقش کاربر مشخص نیست."}, status=status.HTTP_403_FORBIDDEN)

        role = user.main_role.name.lower()

        if role == "student":
            return Response(
                {"message": "شما اجازه ویرایش این کلاس را ندارید."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        elif role == "teacher":
            if section.teacher != user:
                return Response(
                    {"message": "شما فقط می‌توانید کلاس‌های خودتان را ویرایش کنید."}, 
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.get_serializer(instance=section, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"message": "کلاس با موفقیت ویرایش شد."}, status=status.HTTP_200_OK)

class SectionCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionCreateSerializer
    queryset = Section.objects.all()
    
    def post(self, request, *args, **kwargs):
        user = request.user
        
        if not user.main_role:
             return Response({"message": "نقش کاربر مشخص نیست."}, status=status.HTTP_403_FORBIDDEN)

        role = user.main_role.name.lower()
        
        if role not in ["teacher", "superadmin"]:
            return Response(
                {"message": "شما دسترسی لازم برای ایجاد کلاس را ندارید."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        section = serializer.save()
        
        return Response({"message": "کلاس با موفقیت ایجاد شد."}, status=status.HTTP_201_CREATED)

class SetSectionImageViewSet(viewsets.ModelViewSet):
    http_method_names = ['put']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetSectionImageSerializer
    queryset = Section.objects.all()
    lookup_field = 'section_id'
    
    def put(self, request, *args, **kwargs):
        short_id = self.kwargs.get(self.lookup_field)
        user = request.user

        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            return Response(
                {"message": "شناسه کلاس (section ID) نامعتبر است."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            section = Section.objects.get(section_id=section_uuid)
        except Section.DoesNotExist:
            return Response({"message": "کلاسی با این مشخصات وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)    
        
        if not user.main_role:
             return Response({"message": "نقش کاربر مشخص نیست."}, status=status.HTTP_403_FORBIDDEN)

        role = user.main_role.name.lower()

        if role == "student":
            return Response(
                {"message": "شما اجازه تغییر تصویر کلاس را ندارید."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        elif role == "teacher":
            if section.teacher != user:
                return Response(
                    {"message": "شما اجازه ویرایش تصویر این کلاس را ندارید."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        
        serializer = self.get_serializer(instance=section, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"message": "تصویر با موفقیت ویرایش شد."}, status=status.HTTP_200_OK)

class StudentSectionCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSectionSerializer
    queryset = StudentSection.objects.all()
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        student_section = serializer.save()
        
        data = {
            "data": {
                "section": base64.urlsafe_b64encode(student_section.section.section_id.bytes).rstrip(b'=').decode('ascii'),
                "student": student_section.student.personal_number,
                "student_status": student_section.student_status,
            },
            "message": "ثبت نام دانشجو با موفقیت انجام شد."
        }
        return Response(data, status=status.HTTP_201_CREATED)

class StudentSectionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSectionListSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if not user.main_role or user.main_role.name.lower() != 'student':
            return StudentSection.objects.none()
            
        return StudentSection.objects.filter(student=user)

class StudentSectionRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSectionRetrieveSerializer
    lookup_field = 'section_id'
    
    def get_object(self):
        """
        این متد مسئول پیدا کردن آبجکت دقیق است.
        """
        short_id = self.kwargs.get(self.lookup_field)
        user = self.request.user
        
        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            raise ValidationError({"detail": "شناسه کلاس نامعتبر است."})

        if not user.main_role or user.main_role.name.lower() != 'student':
             self.permission_denied(self.request, message="Only students can access this info.")

        queryset = StudentSection.objects.filter(
            section__section_id=section_uuid, 
            student=user
        )
        
        obj = get_object_or_404(queryset)
        
        self.check_object_permissions(self.request, obj)
        return obj
    
class StudentSectionRemoveView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSectionRemoveSerializer
    
    def post(self, request, *args, **kwargs):
        # ارسال context برای دسترسی به user در سریالایزر
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # عملیات حذف در متد save سریالایزر انجام می‌شود
        serializer.save()
        
        return Response({"message": "دانشجو با موفقیت از کلاس حذف شد."}, status=status.HTTP_200_OK)

class MembersSectionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MembersSectionSerializer
    
    def get_queryset(self):
        short_id = self.kwargs.get('section_id')
        user = self.request.user
        
        # 1. دیکود کردن ID
        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            raise ValidationError({"detail": "شناسه کلاس نامعتبر است."})

        # 2. پیدا کردن کلاس
        # از get_object_or_404 استفاده می‌کنیم تا اگر نبود خودکار 404 بدهد
        section = get_object_or_404(Section, section_id=section_uuid)
        
        # 3. بررسی دسترسی (Security Logic)
        # الف) اگر کاربر سوپر ادمین است -> دسترسی دارد
        # ب) اگر کاربر معلمِ همین کلاس است -> دسترسی دارد
        # ج) اگر کاربر دانشجوی عضو همین کلاس است -> دسترسی دارد
        
        is_teacher = (user == section.teacher)
        is_student = StudentSection.objects.filter(section=section, student=user).exists()
        is_admin = (user.main_role and user.main_role.name.lower() == 'superadmin')

        if not (is_teacher or is_student or is_admin):
             raise PermissionDenied("شما عضو این کلاس نیستید و اجازه دیدن اعضا را ندارید.")

        # 4. کوئری اصلی (بهینه شده)
        # نکته کلیدی: استفاده از select_related برای جلوگیری از N+1 Query
        return StudentSection.objects.filter(section=section).select_related('student')

class SemesterViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SemesterSerializer
    
    queryset = Semester.objects.all().order_by('-code')
    
    lookup_field = 'code'
    lookup_value_regex = '[^/]+'
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['code', 'start_date']

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubjectSerializer
    
    queryset = Subject.objects.all().order_by('persian_name')
    
    lookup_field = 'english_name'
    lookup_value_regex = '[^/]+'
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['english_name', 'persian_name', 'description']
    ordering_fields = ['unit', 'persian_name']

class StudentSubjectCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSubjectSerializer
    queryset = StudentSubject.objects.all()
    
    def post(self, request, *args, **kwargs):
        user = request.user
        
        if not user.main_role or user.main_role.name.lower() != "superadmin":
             return Response(
                 {"message": "شما اجازه دسترسی به این بخش را ندارید."}, 
                 status=status.HTTP_403_FORBIDDEN
             )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_subject = serializer.save()
        
        data = {
            "data": {
                "subject": student_subject.subject.english_name,
                "student": student_subject.student.personal_number,
                "access_status": student_subject.access_status
            },
            "message": "دسترسی درس با موفقیت برای دانشجو ایجاد شد."
        }
        return Response(data, status=status.HTTP_201_CREATED)

class StudentSubjectListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSubjectListSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if not user.main_role or user.main_role.name.lower() != 'student':
            return StudentSubject.objects.none()

        return StudentSubject.objects.filter(student=user).select_related('subject')
    
class StudentSubjectRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSubjectRetrieveSerializer
    lookup_url_kwarg = 'english_name' 
    
    def get_object(self):
        subject_name = self.kwargs.get(self.lookup_url_kwarg)
        user = self.request.user
        
        queryset = StudentSubject.objects.filter(
            student=user,
            subject__english_name=subject_name
        ).select_related('subject')
        
        obj = get_object_or_404(queryset)
        
        self.check_object_permissions(self.request, obj)
        return obj
    
class HospitalViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HospitalSerializer
    
    queryset = Hospital.objects.all().order_by('persian_name')
    
    lookup_field = 'english_name'
    lookup_value_regex = '[^/]+'
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    search_fields = [
        'english_name', 
        'persian_name', 
        'city', 
        'province', 
        'description'
    ]
    
    ordering_fields = ['capacity', 'city', 'province']

class HospitalSubjectCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HospitalSubjectSerializer
    queryset = HospitalSubject.objects.all()
    
    def post(self, request):
        user = request.user
        
        # 1. بررسی سطح دسترسی (فقط سوپر ادمین)
        # اتصال بیمارستان به درس یک تنظیمات سیستمی است و نباید توسط همه انجام شود.
        if not user.main_role or user.main_role.name.lower() != "superadmin":
             return Response(
                 {"message": "شما اجازه دسترسی به این بخش را ندارید."}, 
                 status=status.HTTP_403_FORBIDDEN
             )

        # 2. اعتبارسنجی اولیه
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 3. ذخیره‌سازی و مدیریت باگ سریالایزر
        # چون سریالایزر ممکن است به جای آبجکت، یک رشته (String) برگرداند،
        # باید اینجا چک کنیم تا برنامه کرش نکند.
        result = serializer.save()
        
        if isinstance(result, str):
            # اگر خروجی متن بود، یعنی ارور "یافت نشد" در سریالایزر رخ داده
            return Response({"message": result}, status=status.HTTP_400_BAD_REQUEST)
        
        # اگر خروجی آبجکت بود، یعنی همه چیز درست است
        hospital_subject = result
        
        data = {
            "data": {
                "subject": hospital_subject.subject.english_name,
                "hospital": hospital_subject.hospital.english_name,
                "access_status": hospital_subject.access_status
            },
            "message": "ثبت اطلاعات با موفقیت انجام شد."
        }
        return Response(data, status=status.HTTP_201_CREATED)

class HospitalSubjectListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HospitalSubjectListSerializer
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    search_fields = [
        'subject__english_name', 
        'subject__persian_name',
        'hospital__english_name', 
        'hospital__persian_name'
    ]
    
    ordering_fields = ['hospital__english_name', 'subject__english_name']

    def get_queryset(self):
        queryset = HospitalSubject.objects.select_related('subject', 'hospital').all()
        
        subject_name = self.request.query_params.get('subject')
        hospital_name = self.request.query_params.get('hospital')

        if subject_name:
            queryset = queryset.filter(subject__english_name=subject_name)
            
        if hospital_name:
            queryset = queryset.filter(hospital__english_name=hospital_name)
        
        return queryset.order_by('subject__english_name')
    
class HospitalSubjectRetrieveView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HospitalSubjectRetrieveSerializer
    
    lookup_field = 'subject'

    def get_queryset(self):
        subject_name = self.kwargs.get(self.lookup_field)
        
        if not Subject.objects.filter(english_name=subject_name).exists():
            raise NotFound({"message": "Subject does not exist."})

        return HospitalSubject.objects.filter(
            subject__english_name=subject_name
        ).select_related('subject', 'hospital')

