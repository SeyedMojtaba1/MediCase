from .models import ScenarioTemplate, UserScenarioAttempt, StudentLog, PulmonologyFeedback, PulmonologyDisease
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import secrets
import string
from django.contrib.auth import get_user_model

User = get_user_model()

User = get_user_model()

ALPHABET = string.ascii_uppercase + string.digits

def generate_tracking_code(length: int = 10) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

class ScenarioCreateSerializer(serializers.Serializer):
    tracking_code = serializers.CharField()
    
class ScenarioRetrieveSerializer(serializers.ModelSerializer):
    scenario = serializers.JSONField(source='content') 
    
    class Meta:
        model = ScenarioTemplate
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
    feedback = serializers.JSONField(source='feedback_content')
    
    class Meta:
        model = PulmonologyFeedback
        fields = [
            'feedback',
        ]
        
class FeedbackListSerializer(serializers.ModelSerializer):
    scenario_tracking_code = serializers.CharField(
        source='attempt.scenario_template.tracking_code', 
        read_only=True
    )
    
    class Meta:
        model = PulmonologyFeedback
        fields = [
            'feedback_id',
            'scenario_tracking_code',
            'generated'
        ]

class StudentScenarioRankSerializer(serializers.ModelSerializer):
    completed_scenarios_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'completed_scenarios_count']
        
class SectionLeaderboardSerializer(serializers.ModelSerializer):
    top_score = serializers.FloatField()

    class Meta:
        model = User
        fields = ['username', 'top_score']

class RankingInputSerializer(serializers.Serializer):
    section_id = serializers.CharField(max_length=20)
    date = serializers.DateField(required=False)
    subject = serializers.CharField(required=False)

class RankingOutputSerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField()
    score = serializers.IntegerField()
    university_name = serializers.CharField(source='university.english_name', read_only=True, default="Unknown")

    class Meta:
        model = User
        fields = [
            'rank',
            'username',
            'profile_image',
            'score',
            'university_name',
        ]
