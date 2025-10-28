from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from .serializer import (
    SectionSerializer, 
    SemesterSerializer, 
    SubjectSerializer, 
    StudentSubjectSerializer,
    StudentSubjectListSerializer,
    StudentSubjectRetrieveSerializer,
)
from .models import Section, Semester, Subject, StudentSubject
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from rest_framework.decorators import action

class SectionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'
    @method_decorator(cache_page(20 * 60, cache="api_cache"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
        
        print(self.get_queryset())
        
        queryset = self.get_queryset().filter(student=self.request.user, subject=subject.subject_id).first()
        serializer = StudentSubjectListSerializer(queryset)
        
        return Response(serializer.data)
    