from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class PulmonologyDisease(models.Model):
    disease_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    english_name = models.CharField(max_length=50, default=None)
    persian_name = models.CharField(max_length=50, default=None)
    type_disease = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.english_name

class ParaclinicTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    persian_name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    optimal_cost = models.IntegerField(help_text="هزینه ایده‌آل برای امتیازدهی")
    min_cost = models.IntegerField(default=0)
    max_cost = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class ScenarioTemplate(models.Model):
    template_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.JSONField(verbose_name="Scenario Logic JSON") 
    tracking_code = models.CharField(max_length=50, unique=True, db_index=True)
    disease = models.ForeignKey(
        PulmonologyDisease, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="scenarios"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.tracking_code})"

class UserScenarioAttempt(models.Model):
    attempt_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    scenario_template = models.ForeignKey(ScenarioTemplate, on_delete=models.CASCADE, related_name="attempts")
    is_done = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time']

class StudentLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(UserScenarioAttempt, on_delete=models.CASCADE, null=True, related_name="logs")    
    action_log = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

class PulmonologyFeedback(models.Model):
    feedback_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(UserScenarioAttempt, on_delete=models.CASCADE, null=True, related_name="feedbacks")
    feedback_content = models.JSONField(default=dict)
    generated = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)