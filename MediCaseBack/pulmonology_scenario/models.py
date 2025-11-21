from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class PulmonologyDisease(models.Model):
    disease_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    english_name = models.CharField(max_length=50, default=None, unique=True)
    persian_name = models.CharField(max_length=50, default=None, unique=True)


class OptimalCostPulmonologyParaclinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    english_name = models.CharField(max_length=50, default=None, unique=True)
    persian_name = models.CharField(max_length=50, default=None, unique=True)
    optimal_cost = models.IntegerField()

class CostPulmonologyParaclinic(models.Model):
    pulmonologyparaclinic_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug_name = models.CharField(max_length=50, default=None, unique=True)
    name = models.CharField(max_length=50, default=None, unique=True)
    min_cost = models.IntegerField()
    max_cost = models.IntegerField()
    
class PulmonologyScenario(models.Model):
    scenario_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    scenario = models.JSONField()
    tracking_code = models.CharField(blank=True, max_length=10)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="userPulmonologyScenario")
    created_date = models.DateTimeField(auto_now_add=True)

class StudentLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    student_log = models.JSONField()
    scenario = models.ForeignKey(PulmonologyScenario, on_delete=models.SET_NULL, null=True, related_name="studentlog")
    created_date = models.DateTimeField(auto_now_add=True)

class PulmonologyFeedback(models.Model):
    feedback_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    feedback = models.JSONField()
    created_date = models.DateTimeField(auto_now_add=True)
    