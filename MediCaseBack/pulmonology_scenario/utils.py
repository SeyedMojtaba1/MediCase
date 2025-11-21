from celery import shared_task
from .scenario_creator import scenario_creator
from .models import PulmonologyScenario
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()

@shared_task
def senario_creator_celery(user, tracking_code):
    scenario = scenario_creator()
    
    try:
        user = User.objects.get(personal_number=user)
    except User.DoesNotExist:
        return Response(
            {"detail": "User is not exist."}
        )
    
    PulmonologyScenario.objects.get_or_create(
        scenario = scenario,
        tracking_code = tracking_code,
        user = user
    )
    
    user.scenario_credit -= 1
    user.done_scenarios += 1
    user.save()
    scenario.save()
    