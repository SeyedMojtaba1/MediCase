from rest_framework import viewsets, permissions, filters
from rest_framework import permissions
from .serializer import UniversitySerializer, FacultySerializer, DepartmentSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import University, Faculty, Department
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator

class BaseCatalogViewSet(ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    lookup_value_regex = '[^/]+'

    @method_decorator(cache_page(300, key_prefix="catalog_api", cache="api_cache"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UniversityViewSet(BaseCatalogViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    lookup_field = 'english_name'
    search_fields = ['english_name', 'persian_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if not user.main_role:
             return queryset.none()
             
        role = user.main_role.name.lower()

        if role == 'superadmin':
            return queryset
        
        if user.university:
            return queryset.filter(pk=user.university.pk)
            
        return queryset.none()

class FacultyViewSet(BaseCatalogViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    lookup_field = 'name'
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.main_role:
             return queryset.none()

        role = user.main_role.name.lower()

        if role == 'superadmin':
            return queryset

        if user.university:
            return queryset.filter(university=user.university)
        
        return queryset.none()

class DepartmentViewSet(BaseCatalogViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'name'
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.main_role:
             return queryset.none()

        role = user.main_role.name.lower()

        if role == 'superadmin':
            return queryset

        if user.university:
            return queryset.filter(faculty__university=user.university)
        
        return queryset.none()