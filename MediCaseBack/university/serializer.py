from rest_framework import serializers
from .models import University, Faculty, Department

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = [
            'english_name',
            'persian_name',
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
        
# 1. اصلاح ارث‌بری: استفاده از ModelSerializer
class FacultySerializer(serializers.ModelSerializer):
    university = serializers.HyperlinkedRelatedField(
        view_name='university-detail',
        read_only=True,
        lookup_field='english_name'  # 2. اضافه کردن lookup_field مربوط به دانشگاه
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

class DepartmentSerializer(serializers.ModelSerializer):
    faculty = serializers.HyperlinkedRelatedField(
        view_name='faculty-detail',
        read_only=True,
        lookup_field='name'  # 3. اضافه کردن lookup_field مربوط به دانشکده
    )
    
    class Meta:
        model = Department
        fields = [
            'faculty',
            'name',
            'head_of_department'
        ]