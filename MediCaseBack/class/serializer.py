from rest_framework import serializers
from .models import Section, Semester, Subject, StudentSubject
from django.contrib.auth import get_user_model

User = get_user_model()

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
            'english_name',
            'persian_name',
            'unit',
            'description',
            'subject_image',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'english_name'}
        }

class StudentSubjectSerializer(serializers.ModelSerializer):
    subject = serializers.CharField()
    student = serializers.CharField()
    
    class Meta:
        model = StudentSubject
        fields = [
            'subject',
            'student',
            'access_status',
        ]
           
    def create(self, validated_data):
        subject=validated_data['subject']
        student=validated_data['student']
        try:
            subject = Subject.objects.get(english_name=subject)
        except Subject.DoesNotExist:
            return "Subject is not exist."
            
        try:
            student = User.objects.get(personal_number=student)
        except User.DoesNotExist:
            return "Student is not exist."
        
        if StudentSubject.objects.filter(subject=subject, student=student).exists():
            raise serializers.ValidationError(
                {"detail": "This student is already registered for this subject."}
            )
        
        student_subject = StudentSubject.objects.create(
            subject=subject,
            student=student,
            access_status=validated_data['access_status'],
        )
        
        student_subject.save()
        
        return student_subject

class StudentSubjectListSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    
    class Meta:
        model = StudentSubject
        fields = [
            'subject',
            'student',
            'access_status',
        ]

class StudentSubjectRetrieveSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    
    class Meta:
        model = StudentSubject
        fields = [
            'subject',
            'student',
            'access_status',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'subject'}
        }