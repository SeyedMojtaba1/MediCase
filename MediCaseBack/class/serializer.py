from rest_framework import serializers
from .models import Section, StudentSection, Semester, Subject, StudentSubject
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class SectionSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(source='teacher.personal_number', read_only=True)
    semester_code = serializers.CharField(source='semester.code', read_only=True)
    semester_name = serializers.CharField(source='semester.name', read_only=True)
    
    class Meta:
        model = Section
        fields = [
            'section_id',
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
            'url': {'lookup_field': 'section_id'}
        }

class SectionUpdateSerializer(serializers.ModelSerializer):
    new_name = serializers.CharField(write_only=True)
    semester_code = serializers.CharField(write_only=True)
    semester = serializers.CharField(source='semester.code', read_only=True)
    
    class Meta:
        model = Section
        fields = [
            'section_id',
            'new_name',
            'semester_code',
            'semester',
            'start_date',
            'end_date',
            'description',
        ]
        
    def update(self, instance, validated_data):
        request = self.context.get('request')
        teacher = request.user

        semester_code=validated_data["semester_code"]
        
        if not teacher.main_role or teacher.main_role.name.lower() != "teacher":
            raise serializers.ValidationError({"detail": "This user is not assigned as a teacher."})

        try:
            semester = Semester.objects.get(code=semester_code)
        except Semester.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "Semester is not exist."}
            )
            
        instance.name = validated_data.get("new_name", instance.name)
        instance.semester = semester
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.description = validated_data.get("description", instance.description)
        instance.last_update = timezone.now()

        instance.save()
        return instance

class SectionCreateSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(source='teacher.personal_number', read_only=True)
    semester_code = serializers.CharField()
    subject_name = serializers.CharField()
    
    class Meta:
        model = Section
        fields = [
            'section_id',
            'name',
            'teacher',
            'subject_name',
            'semester_code',
            'status',
            'start_date',
            'end_date',
            'section_image',
            'created_date',
            'last_update',
            'description',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        teacher = request.user
        
        semester_code=validated_data["semester_code"]
        subject_name=validated_data["subject_name"]
        
        try:
            teacher = User.objects.get(personal_number=teacher.personal_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "Teacher is not exist."}
            )

        if not teacher.main_role or teacher.main_role.name.lower() != "teacher":
            raise serializers.ValidationError(
                {"detail": "This user is not assigned as a teacher."}
            )
        
        try:
            semester = Semester.objects.get(code=semester_code)
        except Semester.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "Semester is not exist."}
            )
        
        if Section.objects.filter(name=validated_data["name"], teacher=teacher, semester=semester).exists():
            raise serializers.ValidationError(
                {"detail": "This section is already registered."}
            )
        
        try:
            subject = Subject.objects.get(english_name=subject_name)
        except Subject.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "Subject is not exist."}
            )
        
        section = Section.objects.create(
            name=validated_data["name"],
            teacher=teacher,
            semester=semester,
            subject=subject,
            section_image=subject.subject_image,
            student_count=0,
            status="Created",
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            description=validated_data["description"],
        )
        
        section.save()
        
        return section

class SetSectionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['section_image']
    
    def update(self, instance, validated_data):
        section_image=validated_data['section_image']
        
        instance.section_image = section_image
        
        instance.save()
        return instance

class StudentSectionSerializer(serializers.ModelSerializer):
    section = serializers.CharField()
    student = serializers.CharField()
    
    class Meta:
        model = StudentSection
        fields = [
            'section',
            'student',
            'student_status',
        ]
           
    def create(self, validated_data):
        section=validated_data['section']
        student=validated_data['student']
        try:
            section = Section.objects.get(section_id=section)
        except Section.DoesNotExist:
            return "Section is not exist."
            
        try:
            student = User.objects.get(personal_number=student)
        except User.DoesNotExist:
            return "Student is not exist."
        
        if StudentSection.objects.filter(section=section, student=student).exists():
            raise serializers.ValidationError(
                {"detail": "This student is already registered for this section."}
            )
        
        student_section = StudentSection.objects.create(
            section=section,
            student=student,
            student_status=validated_data['student_status'],
        )
        
        section.student_count=section.student_count+1
        section.save()
        student_section.save()
        
        return student_section

class StudentSectionListSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='section.section_id', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    
    class Meta:
        model = StudentSection
        fields = [
            'section',
            'student',
            'student_status',
        ]

class MembersSectionSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source='student.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student.last_name', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_personal_number = serializers.CharField(source='student.personal_number', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    student_scenario_credit = serializers.CharField(source='student.scenario_credit', read_only=True)
    student_profile_image = serializers.CharField(source='student.profile_image', read_only=True)
    student_main_role = serializers.CharField(source='student.main_role', read_only=True)
    
    class Meta:
        model = StudentSection
        fields = [
            "student_first_name",
            "student_last_name",
            "student_username",
            "student_personal_number",
            "student_email",
            "student_scenario_credit",
            "student_profile_image",
            "student_main_role",
        ]

class StudentSectionRetrieveSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='section.section_id', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    
    class Meta:
        model = StudentSection
        fields = [
            'section',
            'student',
            'student_status',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'section_id'}
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