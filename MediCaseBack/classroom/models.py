import logging
from django.db import models
from registery.models import User
import uuid

logger = logging.getLogger('classroom')

class Semester(models.Model):
    semester_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        try:
            super().save(*args, **kwargs)
            if is_new:
                logger.info(f"New Semester created: {self.name} [{self.code}]")
            else:
                logger.info(f"Semester updated: {self.semester_id}")
        except Exception as e:
            logger.error(f"Error saving Semester {self.code}: {e}", exc_info=True)
            raise e

class Subject(models.Model):
    SUBJECT_STATUS = [
        ('Active', 'A'),
        ('Inactive', 'I'),
    ]
    
    subject_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    english_name = models.CharField(max_length=50, default=None, unique=True)
    persian_name = models.CharField(max_length=50, default=None, unique=True)
    unit = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField(max_length=1000)
    subject_image = models.ImageField(
        upload_to='subject/',
        blank=True,
        null=True,
        default='defaults/default_subject.jpg',
    )
    subject_status = models.CharField(choices=SUBJECT_STATUS, max_length=10)

    def __str__(self):
        return self.english_name

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        try:
            super().save(*args, **kwargs)
            if is_new:
                logger.info(f"New Subject added: {self.english_name} ({self.unit} units)")
            else:
                logger.info(f"Subject updated: {self.english_name}")
        except Exception as e:
            logger.error(f"Error saving Subject {self.english_name}: {e}", exc_info=True)
            raise e

class Section(models.Model):
    CLASS_STATUS = [
        ('Active', 'A'),
        ('Closed', 'Cl'),
        ('Finished', 'F'),
        ('Created', 'Cr'),
    ]
    
    section_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, default=None, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='subjects')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='users')
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, related_name='semesters')
    student_count = models.IntegerField()
    status = models.CharField(max_length=15, choices=CLASS_STATUS)
    start_date = models.DateField()
    end_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    section_image = models.ImageField(
        upload_to='section/',
        blank=True,
        null=True,
    )
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        try:
            super().save(*args, **kwargs)
            teacher_id = self.teacher.user_id if self.teacher else "No Teacher"
            if is_new:
                logger.info(f"New Section created: '{self.name}' for Subject: {self.subject} by Teacher ID: {teacher_id}")
            else:
                logger.info(f"Section '{self.name}' updated. Status: {self.status}")
        except Exception as e:
            logger.error(f"Error saving Section {self.name}: {e}", exc_info=True)
            raise e
    
class StudentSection(models.Model):
    STUDENT_STATUS = [
        ('Active', 'A'),
        ('Blocked', 'B'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, related_name='sectionstudents')
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='studentsections')
    student_status = models.CharField(max_length=10, choices=STUDENT_STATUS)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            logger.info(f"Student {self.student} assigned to Section {self.section} with status {self.student_status}")
        except Exception as e:
            logger.error(f"Error assigning Student to Section: {e}", exc_info=True)
            raise e
    
class StudentSubject(models.Model):
    STUDENT_STATUS = [
        ('Blocked', 'B'),
        ('Active', 'A'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='subjectstudents')
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='studentsubjects')
    access_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            logger.info(f"StudentSubject relation updated: Student {self.student} - Subject {self.subject} - Access: {self.access_status}")
        except Exception as e:
            logger.error(f"Error saving StudentSubject: {e}", exc_info=True)
            raise e

class Hospital(models.Model):
    HOSPITAL_TYPE=[
        ("Public Hospital", "Government Hospital"),
        ("Private Hospital", "Private"),
        ("Social Security Hospital", "Social Security"),
        ("Charitable Hospital", "Charitable"),
        ("Military Hospital", "Military"),
        ("Semi-private Hospital", "Semi-private"),
    ]
    
    hospital_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    english_name = models.CharField(max_length=50, default=None, unique=True)
    persian_name = models.CharField(max_length=50, default=None)
    type = models.CharField(max_length=30, choices=HOSPITAL_TYPE)
    established_year = models.DateField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    hospital_image = models.ImageField(
        upload_to='hospital/',
        blank=True,
        null=True,
    )
    website = models.URLField()
    capacity = models.IntegerField()
    description = models.TextField(blank=True, max_length=500)
    
    def __str__(self):
        return self.english_name

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        try:
            super().save(*args, **kwargs)
            if is_new:
                logger.info(f"New Hospital registered: {self.english_name} ({self.city})")
            else:
                logger.info(f"Hospital info updated: {self.english_name}")
        except Exception as e:
            logger.error(f"Error saving Hospital {self.english_name}: {e}", exc_info=True)
            raise e

class HospitalSubject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='subjecthospitals')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, related_name='hospitalsubjects')
    access_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            logger.info(f"Subject {self.subject} linked to Hospital {self.hospital}. Access: {self.access_status}")
        except Exception as e:
            logger.error(f"Error linking Subject to Hospital: {e}", exc_info=True)
            raise e

class StudentCredit(models.Model):
    credit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subject_credits')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_credits')
    balance = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'subject')

    def __str__(self):
        return f"{self.user} - {self.subject.english_name}: {self.balance}"

class CreditTransaction(models.Model):
    ACTION_TYPES = [
        ('ALLOCATE', 'تخصیص توسط ادمین'),
        ('SPEND', 'هزینه سناریو'),
        ('REFUND', 'بازگشت وجه'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='initiated_transactions') 
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions') 
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True) 
    
    amount = models.IntegerField()
    balance_after = models.IntegerField() 
    
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.amount} ({self.action_type})"