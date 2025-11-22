from django.db import models
from registery.models import User
import uuid, base64

class Semester(models.Model):
    semester_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=25)

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
    description = models.TextField(max_length=1000)
    
class StudentSection(models.Model):
    STUDENT_STATUS = [
        ('Active', 'A'),
        ('Blocked', 'B'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, related_name='sectionstudents')
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='studentsections')
    student_status = models.CharField(max_length=10, choices=STUDENT_STATUS)
    
class StudentSubject(models.Model):
    STUDENT_STATUS = [
        ('Blocked', 'B'),
        ('Active', 'A'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='subjectstudents')
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='studentsubjects')
    access_status = models.BooleanField(default=False)

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
    website = models.URLField()
    capacity = models.IntegerField()
    description = models.TextField(blank=True, max_length=500)
    
    def __str__(self):
        return self.english_name

class HospitalSubject(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='subjecthospitals')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, related_name='hospitalsubjects')
    access_status = models.BooleanField(default=False)