from celery import shared_task
from .models import ScenarioTemplate, PulmonologyDisease
from .scenario_creator import scenario_creator
from .views import generate_tracking_code

@shared_task
def generate_nightly_scenarios_task(count=10):
    generated_count = 0
    for _ in range(count):
        try:
            case_data, disease_name, disease_type = scenario_creator()
            
            disease_obj, _ = PulmonologyDisease.objects.get_or_create(
                english_name=disease_name,
                defaults={'type_disease': disease_type}
            )
            
            tracking_code = generate_tracking_code(10)
            
            ScenarioTemplate.objects.create(
                title=f"Auto-generated {disease_name} Scenario",
                content=case_data,
                tracking_code=tracking_code,
                disease=disease_obj
            )
            generated_count += 1
            
        except Exception as e:
            print(f"[Nightly Task Error]: Failed to generate scenario: {e}")
            
    return f"Successfully generated {generated_count} new scenarios."