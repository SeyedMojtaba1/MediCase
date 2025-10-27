from rest_framework import serializers
from .models import Section, Semester, Subject, StudentSubject

class SectionSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(source='teacher.name', read_only=True)
    semester_code = serializers.CharField(source='semester.code', read_only=True)
    semester_name = serializers.CharField(source='semester.name', read_only=True)
    
    class Meta:
        model = Section
        fields = [
            'name',
            'teacher',
            'semester_code',
            'semester_name',
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
            'code',
            'name',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'code'}
        }

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'name',
            'unit',
            'description',
            'subject_image',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

class StudentSubjectSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.name', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    
    class Meta:
        model = StudentSubject
        fields = [
            'subject',
            'student',
            'access_status',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'student'}
        }