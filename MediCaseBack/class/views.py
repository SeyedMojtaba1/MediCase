from rest_framework import viewsets, generics, permissions, status
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
)
from .models import Section, StudentSection, Semester, Subject, StudentSubject, Hospital
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, NotFound
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
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
        section_uuid = decode_short_uuid(short_id)
        
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
    lookup_value_regex = '[^/]+'
    
    def put(self, request, *args, **kwargs):
        short_id = kwargs.get(self.lookup_field)
        section_uuid = decode_short_uuid(short_id)
        try:
            section = Section.objects.get(section_id=section_uuid)
        except Section.DoesNotExist:
            return Response({"message": "کلاسی با این نام وجود ندارد."}, status=status.HTTP_400_BAD_REQUEST)    
        
        serializer = self.get_serializer(instance=section, data=request.data)
        serializer.is_valid(raise_exception=True)
        section = serializer.save()
        
        return Response({"message": "کلاس با موفقیت ویرایش شد."}, status=status.HTTP_200_OK)

class SectionCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionCreateSerializer
    queryset = Section.objects.all()
    
    def post(self, request):
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
    lookup_value_regex = '[^/]+'
    
    def put(self, request):
        try:
            section = Section.objects.get(section_id=self.lookup_field)
        except Section.DoesNotExist:
            return Response({"message": "کلاسی با این مشخصات وجود ندارد."}, status=status.HTTP_400_BAD_REQUEST)    
        
        if section.teacher != self.request.user:
            raise PermissionDenied("You do not have permission to edit this object.")
        
        serializer = self.get_serializer(instance=section, data=request.data)
        serializer.is_valid(raise_exception=True)
        section = serializer.save()
        
        return Response({"message": "تصویر با موفقیت ویرایش شد."}, status=status.HTTP_200_OK)

class StudentSectionCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSectionSerializer
    queryset = StudentSection.objects.all()
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_section = serializer.save()
        
        data = {
            "data": {
                "section": student_section.section.section_id,
                "student": student_section.student.personal_number,
                "student_status": student_section.student_status,
            },
            "message": "ثبت اطلاعات با موفقیت انجام شد."
        }
        return Response(data, status=status.HTTP_201_CREATED)

class StudentSectionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSectionListSerializer
    queryset = StudentSection.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(student=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StudentSectionRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSectionRetrieveSerializer
    queryset = StudentSection.objects.all()
    lookup_field = 'section_id'
    lookup_url_kwarg = 'section_id'
    lookup_value_regex = '[^/]+'

    def retrieve(self, request, *args, **kwargs):
        short_id = kwargs.get(self.lookup_field)
        section_uuid = decode_short_uuid(short_id)
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get(self.lookup_field)
        
        try:
            section = Section.objects.get(section_id=section_uuid)
        except Section.DoesNotExist:
            return Response({"message": "Section is not exist."})
                
        queryset = self.get_queryset().filter(student=self.request.user, section=section.section_id).first()
        serializer = StudentSectionListSerializer(queryset)
        
        return Response(serializer.data)
    
class StudentSectionRemoveView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSectionRemoveSerializer
    queryset = StudentSection.objects.all()
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        short_id = serializer.data['section']
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
            return Response({"message": "کلاسی با این نام وجود ندارد."}, status=status.HTTP_400_BAD_REQUEST)   
        
        try:
            student = User.objects.get(personal_number=serializer.data['student'])
        except User.DoesNotExist:
            return Response({"message": "کاربری با این مشخصات وجود ندارد."}, status=status.HTTP_400_BAD_REQUEST)   
        
        student_section = self.get_queryset().filter(section=section, student=student)
        if not student_section.exists():
            return Response(
                {"message": "ارتباط بین دانشجو و کلاس وجود ندارد."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        student_section.delete()
        
        return Response({"message": "دانشجو از کلاس حذف شد."}, status=status.HTTP_200_OK)

class MembersSectionListView(generics.ListAPIView):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MembersSectionSerializer
    queryset = StudentSection.objects.all()
    lookup_field = 'section_id'
    lookup_value_regex = '[^/]+'
    
    def list(self, request, *args, **kwargs):
        short_id = self.kwargs.get(self.lookup_field)
        section_uuid = decode_short_uuid(short_id)
        try:
            section = Section.objects.get(section_id=section_uuid)
        except Section.DoesNotExist:
            return Response({"message": "کلاسی با این مشخصات وجود ندارد."}, status=status.HTTP_400_BAD_REQUEST)
        
        if section.teacher.user_id != self.request.user.user_id and not StudentSection.objects.filter(section=section, student=self.request.user).exists():
            return Response(
                {"message": "شما در این کلاس عضویت ندارید."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(section=section)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SemesterViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    lookup_field = 'code'
    lookup_value_regex = '[^/]+'
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SubjectViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    lookup_field = 'english_name'
    lookup_value_regex = '[^/]+'
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class StudentSubjectCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSubjectSerializer
    queryset = StudentSubject.objects.all()
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_subject = serializer.save()
        
        data = {
            "data": {
                "subject": student_subject.subject.english_name,
                "student": student_subject.student.personal_number,
                "access_status": student_subject.access_status
            },
            "message": "ثبت اطلاعات با موفقیت انجام شد."
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
class StudentSubjectListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSubjectListSerializer
    queryset = StudentSubject.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(student=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class StudentSubjectRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSubjectRetrieveSerializer
    queryset = StudentSubject.objects.all()
    lookup_field = 'subject'
    lookup_url_kwarg = 'subject'
    lookup_value_regex = '[^/]+'

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get(self.lookup_field)
        
        try:
            subject = Subject.objects.get(english_name=lookup_value)
        except Subject.DoesNotExist:
            return Response({"message": "Subject is not exist."})
                
        queryset = self.get_queryset().filter(student=self.request.user, subject=subject.subject_id).first()
        serializer = StudentSubjectListSerializer(queryset)
        
        return Response(serializer.data)
    
class HospitalViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    lookup_field = 'english_name'
    lookup_value_regex = '[^/]+'
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)