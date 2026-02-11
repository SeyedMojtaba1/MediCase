import logging
from rest_framework import serializers
from .models import Section, StudentSection, Semester, Subject, StudentSubject, Hospital, HospitalSubject, StudentCredit
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
import base64
from .utils import decode_short_uuid, encode_short_uuid, update_section_statuses
from datetime import date
from celery import shared_task

# ==============================================================================
# Logger Setup
# Ensure 'university' matches the app name defined in settings.py LOGGING config
# ==============================================================================
logger = logging.getLogger('classroom')

User = get_user_model()

class SectionListSerializer(serializers.ModelSerializer):
    section_id = serializers.SerializerMethodField(read_only=True)
    # فیلدهای زیر را به SerializerMethodField تغییر دهید
    teacher = serializers.SerializerMethodField(read_only=True)
    semester_code = serializers.SerializerMethodField(read_only=True)
    semester_name = serializers.SerializerMethodField(read_only=True)
    subject = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Section
        fields = [
            'section_id', 'name', 'teacher', 'subject', 'semester_code', 
            'semester_name', 'student_count', 'status', 'start_date', 
            'end_date', 'created_date', 'last_update', 'section_image', 'description',
        ]
        extra_kwargs = {'url': {'lookup_field': 'section_id'}}
        
    def get_section_id(self, obj):
        if not obj.section_id:
            return None
        try:
            return encode_short_uuid(obj.section_id)
        except Exception as e:
            logger.error(f"Error encoding section_id: {e}")
            return None

    # متدهای جدید برای هندل کردن مقادیر Null
    def get_teacher(self, obj):
        if obj.teacher:
            return obj.teacher.personal_number
        return None

    def get_semester_code(self, obj):
        if obj.semester:
            return obj.semester.code
        return None

    def get_semester_name(self, obj):
        if obj.semester:
            return obj.semester.name
        return None

    def get_subject(self, obj):
        if obj.subject:
            return obj.subject.english_name
        return None

class SectionRetrieveSerializer(serializers.ModelSerializer):
    section_id = serializers.SerializerMethodField()
    teacher = serializers.CharField(source='teacher.personal_number', read_only=True)
    semester_code = serializers.CharField(source='semester.code', read_only=True)
    semester_name = serializers.CharField(source='semester.name', read_only=True)
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    
    class Meta:
        model = Section
        fields = [
            'section_id', 'name', 'teacher', 'subject', 'semester_code', 
            'semester_name', 'student_count', 'status', 'start_date', 
            'end_date', 'created_date', 'last_update', 'section_image', 'description',
        ]
        extra_kwargs = {'url': {'lookup_field': 'section_id'}}

    def get_section_id(self, obj):
        return encode_short_uuid(obj.section_id)

@shared_task
def update_section_statuses_task():
    logger.info("Starting scheduled task: update_section_statuses")
    try:
        update_section_statuses()
        logger.info("Task update_section_statuses completed successfully.")
    except Exception as e:
        logger.error(f"Task update_section_statuses failed: {e}", exc_info=True)

class SectionUpdateSerializer(serializers.ModelSerializer):
    new_name = serializers.CharField(write_only=True)
    semester_code = serializers.CharField(write_only=True)
    semester = serializers.CharField(source='semester.code', read_only=True)
    
    class Meta:
        model = Section
        fields = ['section_id', 'new_name', 'semester_code', 'semester', 'start_date', 'end_date', 'description']
        
    def update(self, instance, validated_data):
        request = self.context.get('request')
        teacher = request.user
        
        logger.info(f"Update attempt for Section {instance.section_id} by user {teacher.username}")

        semester_code = validated_data["semester_code"]
        
        if not teacher.main_role or teacher.main_role.name.lower() != "teacher":
            logger.warning(f"Unauthorized update attempt by non-teacher: {teacher.username}")
            raise serializers.ValidationError({"detail": "This user is not assigned as a teacher."})

        try:
            semester = Semester.objects.get(code=semester_code)
        except Semester.DoesNotExist:
            logger.warning(f"Update failed: Semester code {semester_code} not found.")
            raise serializers.ValidationError({"detail": "Semester is not exist."})
            
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]
        today = date.today()

        if today < start_date:
            status = "Created"
        elif start_date <= today <= end_date:
            status = "Active"
        else:
            status = "Finished"
        
        try:
            instance.name = validated_data.get("new_name", instance.name)
            instance.semester = semester
            instance.start_date = validated_data.get("start_date", instance.start_date)
            instance.end_date = validated_data.get("end_date", instance.end_date)
            instance.status = status
            instance.description = validated_data.get("description", instance.description)
            instance.last_update = timezone.now()

            instance.save()
            logger.info(f"Section {instance.section_id} updated successfully.")
            return instance
        except Exception as e:
            logger.error(f"Error updating section {instance.section_id}: {e}", exc_info=True)
            raise e

class SectionCreateSerializer(serializers.ModelSerializer):
    section_id = serializers.SerializerMethodField()
    # این فیلد فقط برای نمایش نام استاد در خروجی است
    teacher = serializers.CharField(source='teacher.personal_number', read_only=True)
    
    # فیلد‌های ورودی
    semester_code = serializers.CharField(write_only=True)
    subject_name = serializers.CharField(write_only=True)
    
    # فیلد جدید برای گرفتن شماره پرسنلی (اختیاری، چون برای Teacher لازم نیست)
    teacher_number = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Section
        fields = [
            'section_id', 'name', 'teacher', 'teacher_number', 'subject_name', 'semester_code', 
            'start_date', 'end_date', 'created_date', 'last_update', 'description',
        ]
        read_only_fields = ['created_date', 'last_update', 'section_id']

    def get_section_id(self, obj):
        return base64.urlsafe_b64encode(obj.section_id.bytes).rstrip(b'=').decode('ascii')
    
    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        
        # 1. تعیین نقش کاربر
        if not user.main_role:
             raise serializers.ValidationError({"detail": "نقش کاربر مشخص نیست."})
        role = user.main_role.name.lower()

        # 2. منطق تعیین استاد کلاس
        target_teacher = None
        
        if role == 'teacher':
            # اگر کاربر استاد است، خودش استاد کلاس می‌شود
            target_teacher = user
        
        elif role in ['admin', 'superadmin']:
            # اگر ادمین است، باید شماره پرسنلی استاد را بفرستد
            t_number = attrs.get('teacher_number')
            if not t_number:
                raise serializers.ValidationError({"teacher_number": "برای ادمین، وارد کردن شماره پرسنلی استاد الزامی است."})
            
            try:
                target_teacher = User.objects.get(personal_number=t_number)
            except User.DoesNotExist:
                raise serializers.ValidationError({"teacher_number": "استادی با این شماره پرسنلی یافت نشد."})
            
            # چک کردن اینکه استاد واقعاً نقش استاد داشته باشد
            if not target_teacher.main_role or target_teacher.main_role.name.lower() != 'teacher':
                 raise serializers.ValidationError({"teacher_number": "کاربر انتخاب شده نقش استاد ندارد."})

            # محدودیت ادمین: فقط اساتید دانشگاه خودش
            if role == 'admin':
                if target_teacher.university != user.university:
                    raise serializers.ValidationError({"teacher_number": "شما مجاز به تعریف کلاس برای اساتید سایر دانشگاه‌ها نیستید."})
        else:
            raise serializers.ValidationError({"detail": "شما دسترسی ایجاد کلاس ندارید."})

        # ذخیره استاد پیدا شده در attrs برای استفاده در متد create
        attrs['teacher'] = target_teacher

        # 3. اعتبارسنجی تاریخ‌ها
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

        if Section.objects.filter(name=attrs.get("name"), teacher=target_teacher, semester=semester).exists():
            raise serializers.ValidationError({"detail": "این کلاس قبلاً برای این استاد ثبت شده است."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('teacher_number', None)
        
        try:
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
                teacher=validated_data["teacher"], # این مقدار در متد validate ست شده است
                semester=validated_data["semester"],
                subject=subject,
                student_count=0,
                status=status_val,
                section_image=subject.subject_image,
                start_date=start_date,
                end_date=end_date,
                description=validated_data.get("description", ""),
            )
            logger.info(f"Section '{section.name}' created successfully for Teacher {validated_data['teacher'].personal_number}")
            return section
        except Exception as e:
            logger.error(f"Error creating section: {e}", exc_info=True)
            raise e

class SetSectionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['section_image']

class StudentSectionSerializer(serializers.ModelSerializer):
    section = serializers.CharField(help_text="Short UUID of the section") 
    student = serializers.CharField(help_text="Personal Number of the student")
    
    class Meta:
        model = StudentSection
        fields = ['section', 'student']
            
    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        
        # 1. Validation of Section ID
        short_id = attrs.get('section')
        try:
            section_uuid = decode_short_uuid(short_id)
            section = Section.objects.select_related('teacher', 'subject').get(section_id=section_uuid)
        except (ValueError, Section.DoesNotExist):
            logger.warning(f"Add Student: Section {short_id} not found.")
            raise serializers.ValidationError({"section": "کلاس مورد نظر یافت نشد."})

        # 2. Validation of Student Personal Number
        student_number = attrs.get('student')
        try:
            student_obj = User.objects.get(personal_number=student_number)
        except User.DoesNotExist:
            logger.warning(f"Add Student: User {student_number} not found.")
            raise serializers.ValidationError({"student": "دانشجویی با این شماره دانشجویی یافت نشد."})

        # 3. Role-Based Access Control (RBAC)
        if not user.main_role:
             raise serializers.ValidationError({"detail": "نقش کاربر مشخص نیست."})

        role = user.main_role.name.lower()

        # --- Logic for Teacher ---
        if role == 'teacher':
            # استاد فقط می‌تواند به کلاس خودش دانشجو اضافه کند
            if section.teacher != user:
                logger.warning(f"Unauthorized: Teacher {user.email} tried to add student to section {section.name} (Owner: {section.teacher})")
                raise serializers.ValidationError({"detail": "شما اجازه افزودن دانشجو به کلاس سایر اساتید را ندارید."})

        # --- Logic for University Admin ---
        elif role == 'admin':
            # 1. کلاس باید متعلق به دانشگاه ادمین باشد (از طریق استاد کلاس)
            if section.teacher.university != user.university:
                raise serializers.ValidationError({"detail": "شما دسترسی به کلاس‌های دانشگاه‌های دیگر را ندارید."})
            
            # 2. دانشجو باید متعلق به دانشگاه ادمین باشد
            if student_obj.university != user.university:
                 raise serializers.ValidationError({"detail": "شما فقط می‌توانید دانشجویان دانشگاه خودتان را اضافه کنید."})

        # --- Logic for SuperAdmin ---
        elif role == 'superadmin':
            pass # سوپر ادمین دسترسی کامل دارد

        # --- Forbidden Roles (Student, etc.) ---
        else:
            logger.warning(f"Unauthorized: Role {role} tried to enroll a student.")
            raise serializers.ValidationError({"detail": "شما مجوز ثبت‌نام دانشجو در کلاس را ندارید."})

        # 4. Check for Duplicate Enrollment
        if StudentSection.objects.filter(section=section, student=student_obj).exists():
            raise serializers.ValidationError({"detail": "این دانشجو قبلاً در این کلاس ثبت شده است."})

        # 5. Replace simple inputs with Model Objects for create()
        attrs['section'] = section
        attrs['student'] = student_obj
        return attrs

    def create(self, validated_data):
        section = validated_data['section']
        student = validated_data['student']
        
        try:
            with transaction.atomic():
                # الف) ایجاد رکورد ثبت نام در کلاس
                student_section = StudentSection.objects.create(
                    section=section,
                    student=student,
                    student_status="Active",
                )
                
                # ب) ایجاد دسترسی به درس (StudentSubject) اگر وجود نداشته باشد
                # نکته: اگر دانشجو قبلاً این درس را با استاد دیگری داشته، رکورد وجود دارد
                # اما اگر اولین بار است این درس را می‌گیرد، باید ایجاد شود.
                StudentSubject.objects.get_or_create(
                    student=student,
                    subject=section.subject,
                    defaults={'access_status': True}
                )
                
                # ج) افزایش شمارنده دانشجویان کلاس
                section.student_count += 1
                section.save(update_fields=['student_count'])

                # د) (اختیاری) ایجاد رکورد کردیت اولیه برای درس اگر نیاز است
                StudentCredit.objects.get_or_create(
                     user=student,
                     subject=section.subject,
                     defaults={'balance': 0}
                )
                
            logger.info(f"Student {student.personal_number} added to Section {section.name} by {self.context['request'].user.email}")
            return student_section
            
        except Exception as e:
            logger.error(f"Error adding student to section: {e}", exc_info=True)
            raise serializers.ValidationError({"detail": "خطایی در ثبت اطلاعات رخ داده است."})

class StudentSectionListSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='section.section_id', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    class Meta:
        model = StudentSection
        fields = ['section', 'student', 'student_status']

class StudentSectionRetrieveSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='section.section_id', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    class Meta:
        model = StudentSection
        fields = ['section', 'student', 'student_status']
        extra_kwargs = {'url': {'lookup_field': 'section_id'}}

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
                logger.warning(f"Unauthorized removal attempt by teacher {user.username}.")
                raise serializers.ValidationError({"detail": "شما اجازه حذف دانشجو از کلاس سایر اساتید را ندارید."})
        
        elif role == 'student':
            if target_student != user:
                logger.warning(f"Unauthorized removal attempt by student {user.username}.")
                raise serializers.ValidationError({"detail": "شما اجازه حذف سایر دانشجویان را ندارید."})

        try:
            student_section = StudentSection.objects.get(section=section, student=target_student)
        except StudentSection.DoesNotExist:
            raise serializers.ValidationError({"detail": "این دانشجو در این کلاس ثبت‌نام نکرده است."})

        attrs['student_section_instance'] = student_section
        attrs['section_instance'] = section
        attrs['student_instance'] = target_student
        return attrs

    def save(self, **kwargs):
        student_section = self.validated_data['student_section_instance']
        section = self.validated_data['section_instance']
        student = self.validated_data['student_instance']
        
        try:
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
                    StudentSubject.objects.filter(student=student, subject=section.subject).delete()
            
            logger.info(f"Student {student.username} removed from Section {section.name}")
        except Exception as e:
            logger.error(f"Error removing student from section: {e}", exc_info=True)
            raise e

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url']
        extra_kwargs = {'url': {'view_name': 'user-detail'}}

class MembersSectionSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='student.first_name', read_only=True)
    last_name = serializers.CharField(source='student.last_name', read_only=True)
    personal_number = serializers.CharField(source='student.personal_number', read_only=True)
    username = serializers.CharField(source='student.username', read_only=True)
    done_scenarios = serializers.CharField(source='student.done_scenarios', read_only=True)
    profile_image = serializers.CharField(source='student.profile_image', read_only=True)
    main_role = serializers.CharField(source='student.main_role.name', read_only=True)
    
    class Meta:
        model = StudentSection
        fields = ['first_name', 'last_name', 'personal_number', 'username', 'done_scenarios', 'profile_image', 'main_role']

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['code', 'name']
        extra_kwargs = {'url': {'lookup_field': 'code'}}

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['english_name', 'persian_name', 'unit', 'description', 'subject_image']
        extra_kwargs = {'url': {'lookup_field': 'english_name'}}

class StudentSubjectSerializer(serializers.ModelSerializer):
    subject = serializers.CharField()
    student = serializers.CharField()
    
    class Meta:
        model = StudentSubject
        fields = ['subject', 'student', 'access_status']
            
    def validate(self, attrs):
        subject_name = attrs.get('subject')
        try:
            subject_obj = Subject.objects.get(english_name=subject_name)
        except Subject.DoesNotExist:
            raise serializers.ValidationError({"subject": "درس مورد نظر یافت نشد."})
            
        student_number = attrs.get('student')
        try:
            student_obj = User.objects.get(personal_number=student_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"student": "دانشجو مورد نظر یافت نشد."})
        
        if StudentSubject.objects.filter(subject=subject_obj, student=student_obj).exists():
            raise serializers.ValidationError({"detail": "این دانشجو قبلاً به این درس دسترسی داشته است."})
        
        attrs['subject'] = subject_obj
        attrs['student'] = student_obj
        return attrs

    def create(self, validated_data):
        try:
            student_subject = StudentSubject.objects.create(
                subject=validated_data['subject'],
                student=validated_data['student'],
                access_status=validated_data.get('access_status', True),
            )
            logger.info(f"Access granted: Student {validated_data['student'].username} -> Subject {validated_data['subject'].english_name}")
            return student_subject
        except Exception as e:
            logger.error(f"Error creating StudentSubject: {e}", exc_info=True)
            raise e

class StudentSubjectListSerializer(serializers.ModelSerializer):
    english_name = serializers.CharField(source='subject.english_name', read_only=True)
    persian_name = serializers.CharField(source='subject.persian_name', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    class Meta:
        model = StudentSubject
        fields = ['english_name', 'persian_name', 'student', 'access_status']
        
class StudentSubjectRetrieveSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    student = serializers.CharField(source='student.personal_number', read_only=True)
    class Meta:
        model = StudentSubject
        fields = ['subject', 'student', 'access_status']
        extra_kwargs = {'url': {'lookup_field': 'subject'}}

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['english_name', 'persian_name', 'type', 'address', 'city', 'province', 'phone_number', 'email', 'website', 'capacity', 'description']
        extra_kwargs = {'url': {'lookup_field': 'english_name'}}

class HospitalSubjectSerializer(serializers.ModelSerializer):
    subject = serializers.CharField()
    hospital = serializers.CharField()
    
    class Meta:
        model = HospitalSubject
        fields = ['subject', 'hospital', 'access_status']
           
    def create(self, validated_data):
        subject_name = validated_data['subject']
        hospital_name = validated_data['hospital']
        try:
            subject = Subject.objects.get(english_name=subject_name)
        except Subject.DoesNotExist:
            logger.warning(f"Hospital Subject Link: Subject {subject_name} not found.")
            raise serializers.ValidationError({"detail": "Subject is not exist."})
            
        try:
            hospital = Hospital.objects.get(english_name=hospital_name)
        except Hospital.DoesNotExist:
            logger.warning(f"Hospital Subject Link: Hospital {hospital_name} not found.")
            raise serializers.ValidationError({"detail": "Hospital is not exist."})
        
        if HospitalSubject.objects.filter(subject=subject, hospital=hospital).exists():
            raise serializers.ValidationError({"detail": "This hospital is already registered for this subject."})
        
        try:
            hospital_subject = HospitalSubject.objects.create(
                subject=subject,
                hospital=hospital,
                access_status=validated_data['access_status'],
            )
            hospital_subject.save()
            logger.info(f"Subject {subject.english_name} linked to Hospital {hospital.english_name}")
            return hospital_subject
        except Exception as e:
            logger.error(f"Error linking hospital to subject: {e}", exc_info=True)
            raise e
    
class HospitalSubjectListSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    hospital_english = serializers.CharField(source='hospital.english_name', read_only=True)
    hospital_persian = serializers.CharField(source='hospital.persian_name', read_only=True)
    hospital_address = serializers.CharField(source='hospital.address', read_only=True)
    class Meta:
        model = HospitalSubject
        fields = ['subject', 'hospital_english', 'hospital_persian', 'hospital_address', 'access_status']
        
class HospitalSubjectRetrieveSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.english_name', read_only=True)
    hospital = serializers.CharField(source='hospital.english_name', read_only=True)
    class Meta:
        model = HospitalSubject
        fields = ['subject', 'hospital', 'access_status']
        extra_kwargs = {'url': {'lookup_field': 'subject'}}

class StudentCreditSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.english_name')
    subject_name_fa = serializers.ReadOnlyField(source='subject.persian_name')

    class Meta:
        model = StudentCredit
        fields = ['subject_name', 'subject_name_fa', 'balance']
        
class BulkCreditUpdateSerializer(serializers.Serializer):
    amount = serializers.IntegerField(
        required=True, 
        help_text="مقدار اعتباری که باید اضافه یا تنظیم شود (باید عدد باشد)"
    )
    mode = serializers.ChoiceField(
        choices=['add', 'set'], 
        default='add',
        required=False,
        help_text="نوع عملیات: add (افزایش مقدار فعلی) یا set (تغییر کامل به این مقدار)"
    )

class SectionRemoveSerializer(serializers.Serializer):
    section_id = serializers.CharField(
        required=True,
        help_text="شناسه کلاس (به صورت رشته رمزنگاری شده مانند خروجی لیست کلاس‌ها)"
    )

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        short_id = attrs.get('section_id')

        # تبدیل شناسه کوتاه به UUID اصلی
        try:
            section_uuid = decode_short_uuid(short_id)
        except ValueError:
            raise serializers.ValidationError({"section_id": "شناسه کلاس نامعتبر است."})

        # بررسی وجود کلاس
        try:
            section = Section.objects.get(section_id=section_uuid)
        except Section.DoesNotExist:
            raise serializers.ValidationError({"section_id": "کلاسی با این شناسه یافت نشد."})

        # --- بررسی سطح دسترسی کاربر ---
        if not user.main_role:
             raise serializers.ValidationError({"detail": "نقش کاربر مشخص نیست."})

        role = user.main_role.name.lower()

        if role == "student":
            raise serializers.ValidationError({"detail": "شما اجازه بستن کلاس را ندارید."})
        elif role == "teacher":
            if section.teacher != user:
                raise serializers.ValidationError({"detail": "شما فقط می‌توانید کلاس‌های خودتان را ببندید."})
        elif role == "admin":
            if section.teacher and section.teacher.university != user.university:
                raise serializers.ValidationError({"detail": "شما فقط مجاز به بستن کلاس‌های دانشگاه خود هستید."})
        elif role == "superadmin":
            pass # سوپر ادمین به همه چیز دسترسی دارد
        else:
            raise serializers.ValidationError({"detail": "شما دسترسی بستن کلاس را ندارید."})

        attrs['section_instance'] = section
        return attrs

    def save(self, **kwargs):
        section = self.validated_data['section_instance']
        
        # تغییر وضعیت کلاس به Closed (بدون تغییر وضعیت دانشجویان)
        section.status = 'Closed'
        section.save()
            
        return section