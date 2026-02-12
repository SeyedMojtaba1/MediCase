from django.db import models
import uuid
from registery.models import User
from university.models import University
from classroom.models import Section

class Announcement(models.Model):
    SCOPE_CHOICES = [
        ('SYSTEM', 'System Wide'),       # سطح کل سیستم
        ('UNIVERSITY', 'University Wide'), # سطح دانشگاه
        ('SECTION', 'Classroom Section'),  # سطح کلاس درس
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)
    target_university = models.ForeignKey(
        University, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='university_announcements'
    )
    
    target_section = models.ForeignKey(
        Section, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='section_announcements'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.scope})"