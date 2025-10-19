from rest_framework import viewsets
from rest_framework import permissions
from .serializer import UniversitySerializer, FacultySerializer, DepartmentSerializer
from .models import University, Faculty, Department
from rest_framework_simplejwt.authentication import JWTAuthentication

class UniversityViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UniversitySerializer
    queryset = University.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

class FacultyViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

class DepartmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'