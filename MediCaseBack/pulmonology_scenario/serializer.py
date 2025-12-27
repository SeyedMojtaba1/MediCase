from .models import PulmonologyScenario, PulmonologyFeedback
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
        model = PulmonologyScenario
        fields = [
            'scenario'
        ]
        extra_kwargs = {
            "url": {'lookup_field': 'tracking_code'}
        }

class ScenarioListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PulmonologyScenario
        fields = [
            'tracking_code',
            'done'
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
            'scenario_tracking_code'
            'generated'
        ]
