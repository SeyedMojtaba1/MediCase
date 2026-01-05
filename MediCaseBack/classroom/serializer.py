from rest_framework import serializers
from .models import Section, StudentSection, Semester, Subject, StudentSubject, Hospital, HospitalSubject
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
import base64
from .utils import decode_short_uuid, encode_short_uuid, update_section_statuses
from datetime import date
from celery import shared_task

User = get_user_model()

class SectionListSerializer(serializers.ModelSerializer):
    section_id = serializers.SerializerMethodField(read_only=True)
    teacher = serializers.CharField(source='teacher.personal_number', read_only=True)
    semester_code = serializers.CharField(source='semester.code', read_only=True)
    semester_name = serializers.CharField(source='semester.name', read_only=True)
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    
    class Meta:
        model = Section
        fields = [
            'section_id',
            'name',
            'teacher',
            'subject',
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
        
    def get_section_id(self, obj):
        return base64.urlsafe_b64encode(obj.section_id.bytes).rstrip(b'=').decode('ascii')

class SectionRetrieveSerializer(serializers.ModelSerializer):
    section_id = serializers.SerializerMethodField()
    teacher = serializers.CharField(source='teacher.personal_number', read_only=True)
    semester_code = serializers.CharField(source='semester.code', read_only=True)
    semester_name = serializers.CharField(source='semester.name', read_only=True)
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    
    class Meta:
        model = Section
        fields = [
            'section_id',
            'name',
            'teacher',
            'subject',
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

    def get_section_id(self, obj):
        return encode_short_uuid(obj.section_id)

@shared_task
def update_section_statuses_task():
    update_section_statuses()

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
            
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]
        today = date.today()

        if today < start_date:
            status = "Created"
        elif start_date <= today <= end_date:
            status = "Active"
        else:
            status = "Finished"
        
        instance.name = validated_data.get("new_name", instance.name)
        instance.semester = semester
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.status = status
        instance.description = validated_data.get("description", instance.description)
        instance.last_update = timezone.now()

        instance.save()
        return instance

class SectionCreateSerializer(serializers.ModelSerializer):
    section_id = serializers.SerializerMethodField()
    teacher = serializers.CharField(source='teacher.personal_number', read_only=True)
    semester_code = serializers.CharField(write_only=True)
    subject_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Section
        fields = [
            'section_id',
            'name',
            'teacher',
            'subject_name',
            'semester_code',
            'start_date',
            'end_date',
            'created_date',
            'last_update',
            'description',
        ]
        read_only_fields = ['created_date', 'last_update', 'section_id']

    def get_section_id(self, obj):
        return base64.urlsafe_b64encode(obj.section_id.bytes).rstrip(b'=').decode('ascii')
    
    def validate(self, attrs):
        """
        تمام اعتبارسنجی‌ها اینجا انجام می‌شود.
        """
        request = self.context.get('request')
        user = request.user
        
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        
        if end_date < start_date:
            raise serializers.ValidationError({"end_date": "تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد."})

        semester_code = attrs.pop("semester_code")
        try:
            semester = Semester.objects.get(code=semester_code)
            attrs['semester'] = semester
        except Semester.DoesNotExist:
            raise serializers.ValidationError({"semester_code": "ترمی با این کد یافت نشد."})

        subject_name = attrs.pop("subject_name")
        try:
            subject = Subject.objects.get(english_name=subject_name)
            attrs['subject'] = subject
        except Subject.DoesNotExist:
            raise serializers.ValidationError({"subject_name": "درسی با این نام یافت نشد."})

        if Section.objects.filter(
            name=attrs.get("name"), 
            teacher=user, 
            semester=semester
        ).exists():
            raise serializers.ValidationError({"detail": "این کلاس قبلاً برای شما ثبت شده است."})
        
        attrs['teacher'] = user
        
        return attrs

    def create(self, validated_data):
        """
        داده‌های validated_data الان شامل آبجکت‌های Semester و Subject و Teacher است.
        """
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]
        today = date.today()
        subject = validated_data["subject"]

        if today < start_date:
            status_val = "Created"
        elif start_date <= today <= end_date:
            status_val = "Active"
        else:
            status_val = "Finished"
        
        section = Section.objects.create(
            name=validated_data["name"],
            teacher=validated_data["teacher"],
            semester=validated_data["semester"],
            subject=subject,
            student_count=0,
            status=status_val,
            section_image=subject.subject_image,
            start_date=start_date,
            end_date=end_date,
            description=validated_data.get("description", ""),
        )
        
        return section

class SetSectionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['section_image']

class StudentSectionSerializer(serializers.ModelSerializer):
    section = serializers.CharField() 
    student = serializers.CharField()
    
    class Meta:
        model = StudentSection
        fields = ['section', 'student']
            
    def validate(self, attrs):
        """
        تمام بررسی‌های امنیتی و اعتبارسنجی اینجا انجام می‌شود.
        """
        request = self.context.get('request')
        user = request.user
        
        short_id = attrs.get('section')
        try:
            section_uuid = decode_short_uuid(short_id)
            section = Section.objects.get(section_id=section_uuid)
        except (ValueError, Section.DoesNotExist):
            raise serializers.ValidationError({"section": "کلاس مورد نظر یافت نشد."})

        student_number = attrs.get('student')
        try:
            student_obj = User.objects.get(personal_number=student_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"student": "دانشجویی با این شماره یافت نشد."})

        if not user.main_role:
             raise serializers.ValidationError({"detail": "نقش کاربر مشخص نیست."})

        role = user.main_role.name.lower()

        if role == 'teacher':
            if section.teacher != user:
                raise serializers.ValidationError(
                    {"detail": "شما اجازه افزودن دانشجو به کلاس سایر اساتید را ندارید."}
                )
        
        elif role == 'student':
            if student_obj != user:
                raise serializers.ValidationError(
                    {"detail": "شما فقط می‌توانید خودتان را در کلاس ثبت نام کنید."}
                )

        if StudentSection.objects.filter(section=section, student=student_obj).exists():
            raise serializers.ValidationError(
                {"detail": "این دانشجو قبلاً در این کلاس ثبت شده است."}
            )

        attrs['section'] = section
        attrs['student'] = student_obj
        
        return attrs

    def create(self, validated_data):
        section = validated_data['section']
        student = validated_data['student']
        
        with transaction.atomic():
            student_section = StudentSection.objects.create(
                section=section,
                student=student,
                student_status="Active",
            )
            
            if not StudentSubject.objects.filter(student=student, subject=section.subject).exists():
                StudentSubject.objects.create(
                    subject=section.subject,
                    student=student,
                    access_status=True
                )
            
            section.student_count += 1
            section.save()
            
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

class StudentSectionRemoveSerializer(serializers.ModelSerializer):
    student = serializers.CharField()
    section = serializers.CharField()
    
    class Meta:
        model = StudentSection
        fields = ["section", "student"]
            
    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        
        short_id = attrs.get('section')
        try:
            section_uuid = decode_short_uuid(short_id)
            section = Section.objects.get(section_id=section_uuid)
        except (ValueError, Section.DoesNotExist):
            raise serializers.ValidationError({"section": "کلاس مورد نظر یافت نشد."})

        target_student_number = attrs.get('student')
        try:
            target_student = User.objects.get(personal_number=target_student_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"student": "دانشجویی با این شماره یافت نشد."})

        if not user.main_role:
             raise serializers.ValidationError({"detail": "نقش کاربر مشخص نیست."})

        role = user.main_role.name.lower()

        if role == 'teacher':
            if section.teacher != user:
                raise serializers.ValidationError(
                    {"detail": "شما اجازه حذف دانشجو از کلاس سایر اساتید را ندارید."}
                )
        
        elif role == 'student':
            if target_student != user:
                raise serializers.ValidationError(
                    {"detail": "شما اجازه حذف سایر دانشجویان را ندارید."}
                )

        try:
            student_section = StudentSection.objects.get(section=section, student=target_student)
        except StudentSection.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "این دانشجو در این کلاس ثبت‌نام نکرده است."}
            )

        attrs['student_section_instance'] = student_section
        attrs['section_instance'] = section
        attrs['student_instance'] = target_student
        
        return attrs

    def save(self, **kwargs):
        student_section = self.validated_data['student_section_instance']
        section = self.validated_data['section_instance']
        student = self.validated_data['student_instance']
        
        with transaction.atomic():
            student_section.delete()
            
            if section.student_count > 0:
                section.student_count -= 1
                section.save()
            
            has_other_sections = StudentSection.objects.filter(
                student=student, 
                section__subject=section.subject
            ).exclude(id=student_section.id).exists()
            
            if not has_other_sections:
                StudentSubject.objects.filter(
                    student=student, 
                    subject=section.subject
                ).delete()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url']
        extra_kwargs = {
            'url': {'view_name': 'user-detail'}
        }

class MembersSectionSerializer(serializers.ModelSerializer):
    # استفاده از source بسیار عالی است
    first_name = serializers.CharField(source='student.first_name', read_only=True)
    last_name = serializers.CharField(source='student.last_name', read_only=True)
    personal_number = serializers.CharField(source='student.personal_number', read_only=True)
    username = serializers.CharField(source='student.username', read_only=True)
    done_scenarios = serializers.CharField(source='student.done_scenarios', read_only=True)
    profile_image = serializers.CharField(source='student.profile_image', read_only=True)
    main_role = serializers.CharField(source='student.main_role.name', read_only=True)
    
    class Meta:
        model = StudentSection
        fields = [
            'first_name',
            'last_name',
            'personal_number',
            'username',
            'done_scenarios',
            'profile_image',
            'main_role',
        ]

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
    # ورودی‌ها به صورت رشته هستند (نام درس و شماره دانشجویی)
    subject = serializers.CharField()
    student = serializers.CharField()
    
    class Meta:
        model = StudentSubject
        fields = [
            'subject',
            'student',
            'access_status',
        ]
            
    def validate(self, attrs):
        """
        تبدیل ورودی‌های متنی به آبجکت و اعتبارسنجی آن‌ها
        """
        # 1. اعتبارسنجی درس (Subject)
        subject_name = attrs.get('subject')
        try:
            subject_obj = Subject.objects.get(english_name=subject_name)
        except Subject.DoesNotExist:
            raise serializers.ValidationError({"subject": "درس مورد نظر یافت نشد."})
            
        # 2. اعتبارسنجی دانشجو (Student)
        student_number = attrs.get('student')
        try:
            student_obj = User.objects.get(personal_number=student_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"student": "دانشجو مورد نظر یافت نشد."})
        
        # 3. بررسی تکراری نبودن
        if StudentSubject.objects.filter(subject=subject_obj, student=student_obj).exists():
            raise serializers.ValidationError(
                {"detail": "این دانشجو قبلاً به این درس دسترسی داشته است."}
            )
        
        # جایگزینی مقادیر String با آبجکت‌های واقعی در دیکشنری attrs
        attrs['subject'] = subject_obj
        attrs['student'] = student_obj
        
        return attrs

    def create(self, validated_data):
        # اینجا داده‌ها تمیز و آماده هستند
        student_subject = StudentSubject.objects.create(
            subject=validated_data['subject'],
            student=validated_data['student'],
            access_status=validated_data.get('access_status', True),
        )
        return student_subject

class StudentSubjectListSerializer(serializers.ModelSerializer):
    # دریافت اطلاعات کامل‌تر از درس برای نمایش در داشبورد دانشجو
    english_name = serializers.CharField(source='subject.english_name', read_only=True)
    persian_name = serializers.CharField(source='subject.persian_name', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    
    class Meta:
        model = StudentSubject
        fields = [
            'english_name',
            'persian_name',
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

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            'english_name',
            'persian_name',
            'type',
            'address',
            'city',
            'province',
            'phone_number',
            'email',
            'website',
            'capacity',
            'description',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'english_name'}
        }

class HospitalSubjectSerializer(serializers.ModelSerializer):
    subject = serializers.CharField()
    hospital = serializers.CharField()
    
    class Meta:
        model = HospitalSubject
        fields = [
            'subject',
            'hospital',
            'access_status',
        ]
           
    def create(self, validated_data):
        subject=validated_data['subject']
        hospital=validated_data['hospital']
        try:
            subject = Subject.objects.get(english_name=subject)
        except Subject.DoesNotExist:
            return "Subject is not exist."
            
        try:
            hospital = Hospital.objects.get(english_name=hospital)
        except Hospital.DoesNotExist:
            return "Student is not exist."
        
        if HospitalSubject.objects.filter(subject=subject, hospital=hospital).exists():
            raise serializers.ValidationError(
                {"detail": "This hospital is already registered for this subject."}
            )
        
        hospital_subject = HospitalSubject.objects.create(
            subject=subject,
            hospital=hospital,
            access_status=validated_data['access_status'],
        )
        
        hospital_subject.save()
        
        return hospital_subject
    
class HospitalSubjectListSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    hospital_english = serializers.CharField(source='hospital.english_name', read_only=True)
    hospital_persian = serializers.CharField(source='hospital.persian_name', read_only=True)
    hospital_address = serializers.CharField(source='hospital.address', read_only=True)
    
    class Meta:
        model = HospitalSubject
        fields = [
            'subject',
            'hospital_english',
            'hospital_persian',
            'hospital_address',
            'access_status',
        ]
        
class HospitalSubjectRetrieveSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    hospital = serializers.CharField(source='hospital.english_name', read_only=True)
    
    class Meta:
        model = HospitalSubject
        fields = [
            'subject',
            'hospital',
            'access_status',
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'subject'}
        }