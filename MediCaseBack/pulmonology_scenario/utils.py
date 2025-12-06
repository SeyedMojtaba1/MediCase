from celery import shared_task
from .scenario_creator import scenario_creator
from .feedback_generator import feedback_generator
from .models import PulmonologyScenario, PulmonologyDisease, PulmonologyFeedback, StudentLog
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()

@shared_task
def senario_creator_celery(user, tracking_code):
    print("before-call-scenario-creator")
    scenario, target_disease = scenario_creator()
    print(target_disease)
    
    # 1. NEW: Check for error dictionary returned by scenario_creator
    if isinstance(scenario, dict) and "error" in scenario:
        print(f"Scenario creation failed: {scenario['error']}")
        # Returning a dictionary to indicate failure status instead of attempting DB operations
        return {"detail": scenario["error"]}
        
    print("after-call-scenario-creator")
    
    try:
        # Renamed variable to user_obj for clarity
        user_obj = User.objects.get(personal_number=user) 
    except User.DoesNotExist:
        # NOTE: Returning Response objects inside Celery is unusual; usually a dictionary/string is returned.
        return {"detail": "User is not exist."}
    
    try:
        disease = PulmonologyDisease.objects.get(english_name=target_disease)
    except PulmonologyDisease.DoesNotExist:
        return {"detail": "Disease is not exist."}
        
    print("before-PulmonologyScenario")
    
    # 2. FIX: Correctly unpack the tuple from get_or_create
    scenario_obj, created = PulmonologyScenario.objects.get_or_create(
        scenario = scenario,
        tracking_code = tracking_code,
        user = user_obj, # Use user_obj
        disease = disease
    )
    
    print("after-PulmonologyScenario")
    
    # Use user_obj
    user_obj.scenario_credit -= 1
    user_obj.done_scenarios += 1
    user_obj.save()
    
    # Call save on the object, not the tuple
    scenario_obj.save() 
    
    return {"detail": "Scenario created successfully."}

@shared_task
def feedback_creator_celery(feedback_tracking_code, scenario_tracking_code, disease, student_log):
    feedback, evaluation, transition = feedback_generator(disease, student_log)
    
    try:
        scenario = PulmonologyScenario.objects.get(tracking_code=scenario_tracking_code)
    except PulmonologyScenario.DoesNotExist:
        # NOTE: Returning Response objects inside Celery is unusual; returning a dict instead.
        return {"detail": "Scenario is not exist."}
    
    # FIX: Correctly unpack the tuple from get_or_create
    final_student_log_obj, created_log = StudentLog.objects.get_or_create(
        student_log = student_log,
        scenario = scenario
    )
    
    # FIX: Correctly unpack the tuple from get_or_create
    final_feedback_obj, created_feedback = PulmonologyFeedback.objects.get_or_create(
        feedback = feedback,
        evaluation = evaluation, 
        transition = transition,
        tracking_code = feedback_tracking_code,
        scenario = scenario
    )
    
    # Call save() on the object, not the tuple
    final_student_log_obj.save()
    final_feedback_obj.save()
    
    return {"detail": "Feedback created successfully."}