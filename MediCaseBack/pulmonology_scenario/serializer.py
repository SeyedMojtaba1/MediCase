from .models import UserScenarioAttempt, PulmonologyFeedback
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import secrets
import string

User = get_user_model()

ALPHABET = string.ascii_uppercase + string.digits

def generate_tracking_code(length: int = 10) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

class ScenarioCreateSerializer(serializers.Serializer):
    tracking_code = serializers.CharField()
    
class ScenarioRetrieveSerializer(serializers.ModelSerializer):
    scenario = serializers.JSONField()
    
    class Meta:
        model = UserScenarioAttempt
        fields = [
            'scenario'
        ]
        extra_kwargs = {
            "url": {'lookup_field': 'tracking_code'}
        }

class UserScenarioAttemptListSerializer(serializers.ModelSerializer):
    tracking_code = serializers.CharField(source='scenario_template.tracking_code', read_only=True)
    disease_name = serializers.CharField(source='scenario_template.disease.english_name', read_only=True)

    class Meta:
        model = UserScenarioAttempt
        fields = [
            'tracking_code',
            'disease_name',
            'is_done',
            'score',
            'start_time',
        ]

class feedbackCreateSerializer(serializers.Serializer):
    tracking_code = serializers.CharField()
    
class StudentLogSerializer(serializers.Serializer):
    student_log = serializers.JSONField()
    
class FeedbackRetrieveSerializer(serializers.ModelSerializer):
    feedback = serializers.JSONField()
    
    class Meta:
        model = PulmonologyFeedback
        fields = [
            'feedback',
        ]
        extra_kwargs = {
            "url": {'lookup_field': 'tracking_code'}
        }
        
class FeedbackListSerializer(serializers.ModelSerializer):
    scenario_tracking_code = serializers.ReadOnlyField(source='scenario.tracking_code')
    
    class Meta:
        model = PulmonologyFeedback
        fields = [
            'tracking_code',
            'scenario_tracking_code',
            'generated'
        ]

class StudentScenarioRankSerializer(serializers.ModelSerializer):
    completed_scenarios_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'completed_scenarios_count']
        
class SectionLeaderboardSerializer(serializers.ModelSerializer):
    # نمره استخراج شده از ساختار JSON فیدبک
    top_score = serializers.FloatField()

    class Meta:
        model = User
        fields = ['username', 'top_score']