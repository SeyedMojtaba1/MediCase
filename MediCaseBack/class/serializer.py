from rest_framework import serializers
from .models import Section, Semester

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            'name',
            'teacher',
            'semester',
            'student_count',
            'status',
            'start_date',
            'end_date',
            'created_date',
            'last_update',
            'section_image',
            'description',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'year',
            'season',
        ]

