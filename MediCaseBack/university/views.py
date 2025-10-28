from rest_framework import viewsets
from rest_framework import permissions
from .serializer import UniversitySerializer, FacultySerializer, DepartmentSerializer
from .models import University, Faculty, Department
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator

class UniversityViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UniversitySerializer
    queryset = University.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'
    @method_decorator(cache_page(20 * 15, cache="api_cache"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class FacultyViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'
    @method_decorator(cache_page(20 * 15, cache="api_cache"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class DepartmentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'
    @method_decorator(cache_page(20 * 15, cache="api_cache"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
