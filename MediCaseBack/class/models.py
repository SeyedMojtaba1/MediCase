from django.db import models
from registery.models import User
import uuid

class Semester(models.Model):
    semester_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=25)

class Subject(models.Model):
    subject_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    english_name = models.CharField(max_length=50, default=None, unique=True)
    persian_name = models.CharField(max_length=50, default=None, unique=True)
    unit = models.IntegerField()
    description = models.TextField(max_length=1000)
    subject_image = models.URLField(blank=True, null=True)

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
    section_image = models.URLField(blank=True, null=True)
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