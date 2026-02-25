import logging
import base64
from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .serializer import (
    SectionListSerializer,
    SectionRetrieveSerializer, 
    SectionUpdateSerializer,
    SectionCreateSerializer,
    SetSectionImageSerializer,
    StudentSectionSerializer,
    StudentSectionListSerializer,
    StudentSectionRetrieveSerializer,
    StudentSectionRemoveSerializer,
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
    BulkCreditUpdateSerializer,
    SectionRemoveSerializer,
    SingleCreditUpdateSerializer,
)
from .models import (
    Section, 
    StudentSection, 
    Semester, 
    Subject, 
    StudentSubject, 
    Hospital, 
    HospitalSubject, 
    StudentCredit, 
    CreditTransaction,
)
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from django.contrib.auth import get_user_model
from .utils import decode_short_uuid
from django.db import transaction
from registery.permission import IsAdminOrSuperAdmin

logger = logging.getLogger('classroom')

User = get_user_model()

class SectionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionListSerializer
    queryset = Section.objects.all()
    
    def list(self, request, *args, **kwargs):
        user = self.request.user
        
        # اصلاح: user.id -> user.user_id
        logger.debug(f"User {user.user_id} ({user.email}) requested Section List.")

        if not user.main_role:
            # اصلاح: user.id -> user.user_id
            logger.warning(f"User {user.user_id} has no main_role. Returning empty list.")
            queryset = self.get_queryset().none()
        else:
            role = user.main_role.name.lower()
            if role == "superadmin":
                queryset = self.get_queryset()
            elif role == "admin": 
                queryset = self.get_queryset().filter(teacher__university=user.university)
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
            logger.warning(f"Invalid section_id format received: {short_id} from user {user.user_id}")
            return Response(
                {"message": "شناسه کلاس (section ID) نامعتبر است."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        role_obj = getattr(user, 'main_role', None)
        if not role_obj:
            logger.warning(f"User {user.user_id} has no main_role.")
            return Response({"message": "نقش کاربر مشخص نیست."}, status=status.HTTP_403_FORBIDDEN)

        role = role_obj.name.lower()
        queryset = None

        if role == "superadmin":
            queryset = self.get_queryset().filter(section_id=section_uuid).first()
            
        elif role == "admin":
            queryset = self.get_queryset().filter(
                section_id=section_uuid, 
                teacher__university=user.university
            ).first()

        elif role == "teacher":
            queryset = self.get_queryset().filter(teacher=user, section_id=section_uuid).first()
            
        elif role == "student":
            queryset = self.get_queryset().filter(sectionstudents__student=user, section_id=section_uuid).first()
        

        if not queryset:
            logger.warning(f"User {user.user_id} with role {role} attempted to access section {section_uuid} but was denied or not found.")
            return Response({"message": "Section does not exist or you don't have access."}, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info(f"User {user.user_id} successfully retrieved section {section_uuid}.")
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

class SectionUpdateViewSet(viewsets.ModelViewSet):
    http_method_names = ['put']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionUpdateSerializer
    queryset = Section.objects.all() 
    lookup_field = 'section_id'
    
    # توجه: نام متد را از put به update تغییر دادم تا با استاندارد ViewSet همخوانی داشته باشد
    def update(self, request, *args, **kwargs):
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
            logger.error(f"Section Update Failed: Section {section_uuid} not found for user {user.user_id}.")
            return Response({"message": "کلاسی با این نام وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        if not user.main_role:
             return Response({"message": "نقش کاربر مشخص نیست."}, status=status.HTTP_403_FORBIDDEN)

        role = user.main_role.name.lower()

        # --- سطح دسترسی دانشجو ---
        if role == "student":
            logger.warning(f"Unauthorized Update Attempt: Student {user.user_id} tried to update section {section_uuid}.")
            return Response(
                {"message": "شما اجازه ویرایش این کلاس را ندارید."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # --- سطح دسترسی استاد ---
        elif role == "teacher":
            if section.teacher != user:
                logger.warning(f"Unauthorized Update Attempt: Teacher {user.user_id} tried to update section {section_uuid} belonging to another.")
                return Response(
                    {"message": "شما فقط می‌توانید کلاس‌های خودتان را ویرایش کنید."}, 
                    status=status.HTTP_403_FORBIDDEN
                )

        # --- سطح دسترسی ادمین دانشگاه ---
        elif role == "admin":
            # چک می‌کنیم که استادِ کلاس، هم‌دانشگاهیِ ادمین باشد
            # همچنین چک می‌کنیم که کلاس استاد داشته باشد (برای جلوگیری از ارور در کلاس‌های بدون استاد)
            if not section.teacher or section.teacher.university != user.university:
                logger.warning(f"Unauthorized Update Attempt: Admin {user.user_id} tried to update section {section_uuid} from another university.")
                return Response(
                    {"message": "شما فقط مجاز به ویرایش کلاس‌های دانشگاه خود هستید."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # --- سطح دسترسی سوپر ادمین ---
        elif role == "superadmin":
            # سوپر ادمین دسترسی کامل دارد
            pass

        # --- سایر نقش‌ها یا نقش نامعتبر ---
        else:
            return Response({"message": "دسترسی غیرمجاز."}, status=status.HTTP_403_FORBIDDEN)

        # ادامه عملیات آپدیت
        serializer = self.get_serializer(instance=section, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f"Section {section_uuid} updated successfully by User {user.user_id} (Role: {role}).")
        
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
        
        if role not in ["teacher", "superadmin", "admin"]:
            logger.warning(f"Unauthorized Create Attempt: User {user.user_id} with role {role} tried to create a section.")
            return Response(
                {"message": "شما دسترسی لازم برای ایجاد کلاس را ندارید."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        try:
            serializer.is_valid(raise_exception=True)
            section = serializer.save()
            
            logger.info(f"Section created successfully: ID {section.section_id} by User {user.user_id}.")
            return Response({"message": "کلاس با موفقیت ایجاد شد."}, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             logger.error(f"Error creating section: {e}")
             return Response({"message": "خطا در ایجاد کلاس."}, status=status.HTTP_400_BAD_REQUEST)

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
        
        # اصلاح: user.id -> user.user_id
        logger.info(f"Section Image Updated: Section {section_uuid} by User {user.user_id}.")
        
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
                "student_name": f"{student_section.student.first_name} {student_section.student.last_name}",
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
        short_id = self.kwargs.get(self.lookup_field)
        
        # اضافه کردن چک امنیتی
        if not short_id:
            raise ValidationError({"detail": "شناسه کلاس ارسال نشده است."})

        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            raise ValidationError({"detail": "شناسه کلاس نامعتبر است."})

        user = self.request.user

        if not user.main_role or user.main_role.name.lower() != 'student':
             # اصلاح: user.id -> user.user_id
             logger.warning(f"Access Denied: Non-student {user.user_id} tried to retrieve student section info.")
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
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # اصلاح: request.user.id -> request.user.user_id
        logger.info(f"Student removed from section successfully by User {request.user.user_id}.")
        
        return Response({"message": "دانشجو با موفقیت از کلاس حذف شد."}, status=status.HTTP_200_OK)

class MembersSectionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MembersSectionSerializer
    
    def get_queryset(self):
        short_id = self.kwargs.get('section_id') # مطابق نام پارامتر در urls.py
        
        # ۱. چک امنیتی قبل از ارسال به دکودر
        if not short_id:
            logger.error("MembersSectionList: section_id is missing in URL.")
            raise ValidationError({"detail": "شناسه کلاس ارسال نشده است."})

        # ۲. تلاش برای دکود کردن
        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            raise ValidationError({"detail": "شناسه کلاس نامعتبر است."})

        # ۳. ادامه منطق فیلتر کردن (کدهای قبلی شما)
        section = get_object_or_404(Section, section_id=section_uuid)
        user = self.request.user
                
        is_teacher = (user == section.teacher)
        is_student = StudentSection.objects.filter(section=section, student=user).exists()
        is_admin = (user.main_role and user.main_role.name.lower() == 'superadmin')

        if not (is_teacher or is_student or is_admin):
             # اصلاح: user.id -> user.user_id
             logger.warning(f"Access Denied: User {user.user_id} tried to view members of section {section_uuid}.")
             raise PermissionDenied("شما عضو این کلاس نیستید و اجازه دیدن اعضا را ندارید.")

        # اصلاح: user.id -> user.user_id
        logger.info(f"User {user.user_id} retrieved members list for section {section_uuid}.")
        return StudentSection.objects.filter(section=section).select_related('student')
    
    def list(self, request, *args, **kwargs):
        # ۱. دریافت لیست فعلی دانشجویان ثبت‌نام شده
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        members_data = list(serializer.data) # تبدیل ReturnList به لیست پایتون
        
        # ۲. پیدا کردن کلاس و استخراج اطلاعات استاد
        short_id = self.kwargs.get('section_id')
        try:
            section_uuid = decode_short_uuid(short_id)
            section = Section.objects.select_related('teacher').get(section_id=section_uuid)
            
            if section.teacher:
                teacher_data = {
                    "first_name": section.teacher.first_name,
                    "last_name": section.teacher.last_name,
                    "personal_number": section.teacher.personal_number,
                    "username": section.teacher.username,
                    "done_scenarios": str(section.teacher.done_scenarios) if section.teacher.done_scenarios else "0",
                    "profile_image": str(section.teacher.profile_image) if section.teacher.profile_image else None,
                    "main_role": section.teacher.main_role.name if section.teacher.main_role else "Teacher"
                }
                # ۳. استاد را به ابتدای لیست اعضا (ایندکس ۰) اضافه می‌کنیم
                members_data.insert(0, teacher_data)
        except (ValueError, Section.DoesNotExist):
            pass
            
        # ۴. ارسال لیست کامل به کلاینت
        return Response(members_data)

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
             # اصلاح: user.id -> user.user_id
             logger.warning(f"Access Denied: User {user.user_id} tried to create StudentSubject.")
             return Response(
                 {"message": "شما اجازه دسترسی به این بخش را ندارید."}, 
                 status=status.HTTP_403_FORBIDDEN
             )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_subject = serializer.save()
        
        # اصلاح: student.id -> student.user_id و user.id -> user.user_id
        logger.info(f"StudentSubject created: Student {student_subject.student.user_id} -> Subject {student_subject.subject.english_name} by Admin {user.user_id}")
        
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
        
        if not user.main_role or user.main_role.name.lower() != "superadmin":
             # اصلاح: user.id -> user.user_id
             logger.warning(f"Access Denied: User {user.user_id} tried to link Hospital-Subject.")
             return Response(
                 {"message": "شما اجازه دسترسی به این بخش را ندارید."}, 
                 status=status.HTTP_403_FORBIDDEN
             )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        result = serializer.save()
        
        if isinstance(result, str):
            logger.error(f"HospitalSubject Creation Failed: {result}")
            return Response({"message": result}, status=status.HTTP_400_BAD_REQUEST)
        
        hospital_subject = result
        # اصلاح: user.id -> user.user_id
        logger.info(f"HospitalSubject linked: {hospital_subject.hospital.english_name} <-> {hospital_subject.subject.english_name} by Admin {user.user_id}")
        
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
        
        if subject_name is None:
            logger.warning("HospitalSubject Retrieve: No subject provided in URL.")
            return HospitalSubject.objects.none()

        if not Subject.objects.filter(english_name=subject_name).exists():
            logger.warning(f"HospitalSubject Retrieve: Subject {subject_name} does not exist.")
            raise NotFound({"message": "Subject does not exist."})

        return HospitalSubject.objects.filter(
            subject__english_name=subject_name
        ).select_related('subject', 'hospital')
    
class BulkCreditUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=BulkCreditUpdateSerializer,
    )
    def post(self, request, section_id):
        serializer = BulkCreditUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data['amount']
        mode = serializer.validated_data.get('mode', 'add')
        user = request.user

        if not user.main_role:
             return Response({"message": "نقش کاربر مشخص نیست."}, status=status.HTTP_403_FORBIDDEN)
        
        role = user.main_role.name.lower()
        if role not in ['admin', 'superadmin']:
            logger.warning(f"Unauthorized Credit Update: User {user.id} tried to update credits.")
            return Response({"message": "شما اجازه تغییر اعتبار دانشجویان را ندارید."}, status=status.HTTP_403_FORBIDDEN)

        try:
            from .utils import decode_short_uuid
            try:
                section_uuid = decode_short_uuid(section_id)
            except ValueError:
                section_uuid = section_id 

            section = Section.objects.select_related('subject', 'teacher').get(section_id=section_uuid)
        except Section.DoesNotExist:
            return Response({"message": "کلاس مورد نظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        
        if role == 'admin':
            if section.teacher.university != user.university:
                return Response({"message": "شما دسترسی به این کلاس را ندارید."}, status=status.HTTP_403_FORBIDDEN)

        target_subject = section.subject 
        if not target_subject:
             return Response({"error": "این کلاس به هیچ درسی متصل نیست."}, status=status.HTTP_400_BAD_REQUEST)

        student_ids = StudentSection.objects.filter(
            section=section, 
            student_status='Active'
        ).values_list('student_id', flat=True)

        if not student_ids:
            return Response({"message": "دانشجویی در این کلاس یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        updated_count = 0
        try:
            with transaction.atomic():
                for s_id in student_ids:
                    credit_obj, created = StudentCredit.objects.select_for_update().get_or_create(
                        user_id=s_id, 
                        subject=target_subject,
                        defaults={'balance': 0}
                    )
                    
                    old_balance = credit_obj.balance
                    if mode == 'add':
                        credit_obj.balance += amount
                        change_amount = amount
                    elif mode == 'set':
                        change_amount = amount - old_balance
                        credit_obj.balance = amount
                    
                    credit_obj.save()
                    
                    student_user = User.objects.select_for_update().get(pk=s_id)
                    if student_user.scenario_credit is None:
                        student_user.scenario_credit = 0
                    student_user.scenario_credit += change_amount
                    student_user.save()

                    StudentSubject.objects.get_or_create(
                        student=student_user,
                        subject=target_subject,
                        defaults={'access_status': True}
                    )

                    CreditTransaction.objects.create(
                        actor=user,
                        student=student_user,
                        section=section,     
                        amount=change_amount,
                        balance_after=credit_obj.balance,
                        action_type='ALLOCATE',
                        description=f"شارژ گروهی کلاس {section.name}"
                    )
                    
                    updated_count += 1
            
            logger.info(f"Credits Updated: Section {section.section_id}, Subject {target_subject.english_name}, Users Updated: {updated_count}, Mode: {mode}, Amount: {amount}")

        except Exception as e:
            logger.error(f"Error in BulkCreditUpdate: {e}")
            return Response({"message": "خطا در بروزرسانی اعتبار."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": f"اعتبار درس '{target_subject.persian_name}' و کیف پول اصلی {updated_count} دانشجو بروز شد.",
            "subject": target_subject.english_name,
            "mode": mode,
            "amount": amount
        }, status=status.HTTP_200_OK)

class SectionRemoveView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'section_id'
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        short_id = self.kwargs.get(self.lookup_field)
        
        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            logger.warning(f"Invalid section_id format received: {short_id} from user {user.user_id}")
            return Response(
                {"message": "شناسه کلاس (section ID) نامعتبر است."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            section = Section.objects.get(section_id=section_uuid)
        except Section.DoesNotExist:
            return Response({"message": "کلاسی با این مشخصات یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        if not user.main_role:
             return Response({"message": "نقش کاربر مشخص نیست."}, status=status.HTTP_403_FORBIDDEN)

        role = user.main_role.name.lower()
        has_permission = False

        if role == "superadmin":
            has_permission = True
        elif role == "admin":
            if section.teacher and section.teacher.university == user.university:
                has_permission = True
        elif role == "teacher":
            if section.teacher == user:
                has_permission = True
        
        if not has_permission:
            logger.warning(f"Unauthorized Section Close Attempt: User {user.user_id} tried to close section {section_uuid}.")
            return Response({"message": "شما اجازه حذف (بستن) این کلاس را ندارید."}, status=status.HTTP_403_FORBIDDEN)

        try:
            section.status = 'Closed'
            section.save()
            
            logger.info(f"Section {section.section_id} status changed to Closed by User {user.user_id}.")
            return Response(
                {"message": f"وضعیت کلاس '{section.name}' با موفقیت به 'بسته شده' (Closed) تغییر یافت."}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
             logger.error(f"Error closing section: {e}")
             return Response({"message": "خطا در عملیات بستن کلاس."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
class SingleCreditUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=SingleCreditUpdateSerializer,
    )
    def post(self, request):
        serializer = SingleCreditUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        student_number = serializer.validated_data['student_number']
        subject_name = serializer.validated_data['subject_name']
        amount = serializer.validated_data['amount']
        mode = serializer.validated_data['mode']
        custom_desc = serializer.validated_data.get('description', "")

        user = request.user

        if not user.main_role:
             return Response({"message": "نقش کاربر مشخص نیست."}, status=status.HTTP_403_FORBIDDEN)
        
        role = user.main_role.name.lower()
        if role not in ['admin', 'superadmin']:
            logger.warning(f"Unauthorized Single Credit Update: User {user.user_id} tried to update credits.")
            return Response({"message": "شما اجازه تغییر اعتبار دانشجویان را ندارید."}, status=status.HTTP_403_FORBIDDEN)

        try:
            target_student = User.objects.get(personal_number=student_number)
        except User.DoesNotExist:
            return Response({"message": "دانشجویی با این شماره یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        if role == 'admin':
            if target_student.university != user.university:
                return Response({"message": "شما فقط مجاز به تغییر اعتبار دانشجویان دانشگاه خود هستید."}, status=status.HTTP_403_FORBIDDEN)

        try:
            target_subject = Subject.objects.get(english_name=subject_name)
        except Subject.DoesNotExist:
            return Response({"message": "درسی با این نام یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                credit_obj, created = StudentCredit.objects.select_for_update().get_or_create(
                    user=target_student, 
                    subject=target_subject,
                    defaults={'balance': 0}
                )
                
                old_balance = credit_obj.balance
                change_amount = 0

                if mode == 'add':
                    credit_obj.balance += amount
                    change_amount = amount
                elif mode == 'set':
                    change_amount = amount - old_balance
                    credit_obj.balance = amount
                
                credit_obj.save()
                
                student_user = User.objects.select_for_update().get(pk=target_student.pk)
                if student_user.scenario_credit is None:
                    student_user.scenario_credit = 0
                student_user.scenario_credit += change_amount
                student_user.save()

                StudentSubject.objects.get_or_create(
                    student=target_student,
                    subject=target_subject,
                    defaults={'access_status': True}
                )

                description = custom_desc if custom_desc else f"شارژ دستی درس {target_subject.persian_name}"
                CreditTransaction.objects.create(
                    actor=user,
                    student=target_student,
                    section=None,
                    amount=change_amount,
                    balance_after=credit_obj.balance,
                    action_type='ALLOCATE',
                    description=description
                )
            
            logger.info(f"Single Credit Update: Student {student_number}, Subject {subject_name}, Amount {change_amount}, By {user.user_id}")

        except Exception as e:
            logger.error(f"Error in SingleCreditUpdate: {e}")
            return Response({"message": "خطا در بروزرسانی اعتبار."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "اعتبار دانشجو با موفقیت بروزرسانی شد.",
            "student": f"{target_student.first_name} {target_student.last_name}",
            "subject": target_subject.english_name,
            "new_balance": credit_obj.balance,
            "wallet_change": change_amount
        }, status=status.HTTP_200_OK)