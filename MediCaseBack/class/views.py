from rest_framework import viewsets
from rest_framework import permissions
from .serializer import (
    SectionSerializer, 
    SemesterSerializer, 
    SubjectSerializer, 
    StudentSubjectSerializer,
)
from .models import Section, Semester, Subject, StudentSubject
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from rest_framework.decorators import action

class SectionViewSet(viewsets.ModelViewSet):
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'
    @method_decorator(cache_page(20 * 60, cache="api_cache"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class StudentSubjectViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSubjectSerializer
    queryset = StudentSubject.objects.all()
    
    @method_decorator(cache_page(20 * 60, cache="api_cache"))
    @action(detail=False, methods=['get'], url_path='(?P<student>[^/]+)')
    def by_student(self, request, student=None):
        queryset = self.get_queryset().filter(student=student)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)