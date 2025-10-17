from rest_framework import serializers
from .models import University, Faculty, Department

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = [
            'name',
            'type',
            'established_year',
            'address',
            'city',
            'province',
            'phone_number',
            'email',
            'website',
            'rector_name',
            'description',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }
        
class FacultySerializer(serializers.HyperlinkedIdentityField):
    university = serializers.HyperlinkedRelatedField(
        view_name='university-detail',
        read_only=True
    )
    
    class Meta:
        model = Faculty
        fields = [
            'university',
            'name',
            'dean',
            'phone_number',
            'email'
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

class DepartmentSerializer(serializers.ModelSerializer):
    faculty = serializers.HyperlinkedRelatedField(
        view_name='faculty-detail',
        read_only=True
    )
    
    class Meta:
        model = Department
        fields = [
            'faculty',
            'name',
            'head_of_department'
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }