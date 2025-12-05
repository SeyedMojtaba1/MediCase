from celery import shared_task
from .scenario_creator import scenario_creator
from .feedback_generator import feedback_generator
from .models import PulmonologyScenario, PulmonologyDisease, PulmonologyFeedback, StudentLog
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()

@shared_task
def senario_creator_celery(user, tracking_code):
    scenario, target_disease = scenario_creator()
    
    try:
        user = User.objects.get(personal_number=user)
    except User.DoesNotExist:
        return Response(
            {"detail": "User is not exist."}
        )
    
    try:
        disease = PulmonologyDisease.objects.get(english_name=target_disease)
    except PulmonologyDisease.DoesNotExist:
        return Response(
            {"detail": "Disease is not exist."}
        )
    
    scenario = PulmonologyScenario.objects.get_or_create(
        scenario = scenario,
        tracking_code = tracking_code,
        user = user,
        disease = disease
    )
    
    user.scenario_credit -= 1
    user.done_scenarios += 1
    user.save()
    scenario.save()
    
@shared_task
def feedback_creator_celery(feedback_tracking_code, scenario_tracking_code, disease, student_log):
    feedback, evaluation, transition = feedback_generator(disease, student_log)
    
    try:
        scenario = PulmonologyScenario.objects.get(tracking_code=scenario_tracking_code)
    except PulmonologyScenario.DoesNotExist:
        return Response(
            {"detail": "Scenario is not exist."}
        )
    
    final_student_log = StudentLog.objects.get_or_create(
        student_log = student_log,
        scenario = scenario
    )
    
    final_feedback = PulmonologyFeedback.objects.get_or_create(
        feedback = feedback,
        evaluation = evaluation, 
        transition = transition,
        tracking_code = feedback_tracking_code,
        scenario = scenario
    )
    
    final_student_log.save()
    final_feedback.save()