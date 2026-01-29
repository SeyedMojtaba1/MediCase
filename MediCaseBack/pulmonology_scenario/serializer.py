from .models import ScenarioTemplate, UserScenarioAttempt, StudentLog, PulmonologyFeedback, PulmonologyDisease
from rest_framework import serializers
import secrets
import string

ALPHABET = string.ascii_uppercase + string.digits

def generate_tracking_code(length: int = 10) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

class ScenarioCreateSerializer(serializers.Serializer):
    tracking_code = serializers.CharField()
    
class ScenarioRetrieveSerializer(serializers.ModelSerializer):
    # در مدل ScenarioTemplate نام فیلد content است
    scenario = serializers.JSONField(source='content') 
    
    class Meta:
        # تغییر مهم: این ویو اطلاعات تمپلیت را نشان می‌دهد نه تلاش کاربر را
        model = ScenarioTemplate
        fields = [
            'scenario'
        ]
        extra_kwargs = {
            "url": {'lookup_field': 'tracking_code'}
        }

class UserScenarioAttemptListSerializer(serializers.ModelSerializer):
    # مسیر درست: تلاش -> تمپلیت -> کد پیگیری
    tracking_code = serializers.CharField(source='scenario_template.tracking_code', read_only=True)
    disease_name = serializers.CharField(source='scenario_template.disease.english_name', read_only=True)
    title = serializers.CharField(source='scenario_template.title', read_only=True)

    class Meta:
        model = UserScenarioAttempt
        fields = [
            'attempt_id',
            'tracking_code',
            'title',
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
    # در مدل جدید نام فیلد feedback_content است
    feedback = serializers.JSONField(source='feedback_content')
    
    class Meta:
        model = PulmonologyFeedback
        fields = [
            'feedback_id',
            'feedback',
        ]
        # چون فیدبک دیگر ترکینگ کد ندارد، معمولا با ID گرفته می‌شود
        # مگر اینکه در مدل فیدبک فیلد tracking_code را نگه داشته باشید.
        
class FeedbackListSerializer(serializers.ModelSerializer):
    # مسیر بسیار مهم: فیدبک -> تلاش -> تمپلیت -> کد پیگیری
    scenario_tracking_code = serializers.CharField(
        source='attempt.scenario_template.tracking_code', 
        read_only=True
    )
    
    class Meta:
        model = PulmonologyFeedback
        fields = [
            'feedback_id',          # شناسه خود فیدبک
            'scenario_tracking_code', # کد سناریوی مربوطه
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