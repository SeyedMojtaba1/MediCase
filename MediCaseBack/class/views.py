from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from .serializer import (
    SectionSerializer, 
    SectionUpdateSerializer,
    SectionCreateSerializer,
    StudentSectionSerializer,
    StudentSectionRetrieveSerializer,
    StudentSectionListSerializer,
    SemesterSerializer, 
    SubjectSerializer, 
    StudentSubjectSerializer,
    StudentSubjectListSerializer,
    StudentSubjectRetrieveSerializer,
)
from .models import Section, StudentSection, Semester, Subject, StudentSubject
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

User = get_user_model()

class SectionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    lookup_field = 'section_id'
    lookup_value_regex = '[^/]+'
    @method_decorator(cache_page(20 * 60, cache="api_cache"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SectionUpdateViewSet(viewsets.ModelViewSet):
    http_method_names = ['put']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionUpdateSerializer
    queryset = Section.objects.all()
    lookup_field = 'section_id'
    lookup_url_kwarg = 'section_id'
    lookup_value_regex = '[^/]+'
    
    def put(self, request):
        try:
            section = Section.objects.get(section_id=self.lookup_field)
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

    @method_decorator(cache_page(20 * 60, cache="api_cache"))
    @method_decorator(vary_on_headers('Authorization',))
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

    @method_decorator(cache_page(20 * 60, cache="api_cache"))
    @method_decorator(vary_on_headers('Authorization',))
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get(self.lookup_field)
        
        try:
            section = Section.objects.get(section_id=lookup_value)
        except Section.DoesNotExist:
            return Response({"message": "Section is not exist."})
                
        queryset = self.get_queryset().filter(student=self.request.user, section=section.section_id).first()
        serializer = StudentSectionListSerializer(queryset)
        
        return Response(serializer.data)
    
class SemesterViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    lookup_field = 'code'
    lookup_value_regex = '[^/]+'
    
    @method_decorator(cache_page(20 * 60, cache="api_cache"))
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
    
    @method_decorator(cache_page(20 * 60, cache="api_cache"))
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

    @method_decorator(cache_page(20 * 60, cache="api_cache"))
    @method_decorator(vary_on_headers('Authorization',))
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

    @method_decorator(cache_page(20 * 60, cache="api_cache"))
    @method_decorator(vary_on_headers('Authorization',))
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
    