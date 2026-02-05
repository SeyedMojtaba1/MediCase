from rest_framework import viewsets, permissions, filters
from rest_framework import permissions
from .serializer import UniversitySerializer, FacultySerializer, DepartmentSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import University, Faculty, Department
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from registery.models import User
from classroom.models import Section

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

class UniversityDashboardStats(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.main_role.name.lower() != 'admin' or not user.university:
            return Response(status=403)

        uni = user.university
        
        active_students = User.objects.filter(university=uni, main_role__name='Student', is_active=True).count()
        active_teachers = User.objects.filter(university=uni, main_role__name='Teacher', is_active=True).count()
        active_sections = Section.objects.filter(teacher__university=uni, status='Active').count()
        
        return Response({
            "university": uni.persian_name,
            "stats": {
                "students": active_students,
                "teachers": active_teachers,
                "active_classes": active_sections,
            }
        })