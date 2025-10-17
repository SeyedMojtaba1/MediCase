from rest_framework import viewsets
from rest_framework import permissions
from .serializer import UniversitySerializer, FacultySerializer, DepartmentSerializer
from .models import University, Faculty, Department

class UniversityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UniversitySerializer
    queryset = University.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

class FacultyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'