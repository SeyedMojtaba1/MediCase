from django.db import models
import uuid

class University(models.Model):
    UNIVERSITY_TYPES=[
        ("Public University", "Public"),
        ("Islamic Azad University", "Islamic Azad"),
        ("Non-Profit Non-Governmental University", "Non-Profit Non-Governmental"),
        ("Payame Noor University", "Payame Noor", "Open/Distance University", "Open/Distance"),
        ("University of Applied Science and Technology"),
        ("Technical and Vocational University", "Technical and Vocational")
    ]
    
    university_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, default=None, unique=True)
    type = models.CharField(choices=UNIVERSITY_TYPES),
    established_year = models.DateField()
    address = models.TextField(max_length=250)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    website = models.URLField()
    rector_name = models.CharField(max_length=80)
    description = models.TextField(blank=True, max_length=500)
    
    def __str__(self):
        return self.name
    
class Faculty(models.Model):
    faculty_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, related_name='faculties')
    name = models.CharField(max_length=50)
    dean = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    
    def __str__(self):
        return self.name
    
class Department(models.Model):
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='departments')
    name = models.CharField(max_length=50)
    head_of_department = models.CharField(max_length=80)

    def __str__(self):
        return self.name