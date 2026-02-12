from django.db import models
import uuid

class Tutorial(models.Model):
    tutorial_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TutorialPage(models.Model):
    page_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.tutorial.title})"