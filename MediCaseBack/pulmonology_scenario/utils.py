from celery import shared_task
from .scenario_creator import scenario_creator
from .feedback_utils.generate_feedback import generate_feedback
from .models import PulmonologyScenario, PulmonologyDisease, PulmonologyFeedback, StudentLog
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task
def senario_creator_celery(personal_number, tracking_code):
    scenario_data, target_disease, type_disease = scenario_creator()
    
    if isinstance(scenario_data, dict) and "error" in scenario_data:
        return {"detail": scenario_data["error"]}
        
    try:
        # استفاده از transaction.atomic برای امنیت داده‌ها
        with transaction.atomic():
            # ۱. پیدا کردن کاربر و قفل کردن ردیف برای جلوگیری از Race Condition
            try:
                user_obj = User.objects.select_for_update().get(personal_number=personal_number)
            except User.DoesNotExist:
                return {"detail": "User does not exist."}
            
            # ۲. پیدا کردن بیماری
            try:
                disease = PulmonologyDisease.objects.get(
                    english_name=target_disease, 
                    type_disease=type_disease
                )
            except PulmonologyDisease.DoesNotExist:
                return {"detail": "Disease does not exist."}
            
            # ۳. ایجاد سناریو (فقط با کد رهگیری چک می‌کنیم که تکراری نباشد)
            scenario_obj, created = PulmonologyScenario.objects.get_or_create(
                tracking_code=tracking_code,
                defaults={
                    'scenario': scenario_data,
                    'user': user_obj,
                    'disease': disease
                }
            )
            
            if created:
                # ۴. بروزرسانی اعتبار با استفاده از F() برای جلوگیری از تداخل
                user_obj.scenario_credit = F('scenario_credit') - 1
                user_obj.done_scenarios = F('done_scenarios') + 1
                user_obj.save()
                
                return {"detail": "Scenario created successfully."}
            else:
                return {"detail": "Scenario with this tracking code already exists."}

    except Exception as e:
        logger.error(f"Error in scenario creation: {str(e)}")
        return {"detail": "An internal error occurred."}
    
@shared_task
def feedback_creator_celery(feedback_tracking_code, scenario_tracking_code, disease, type_disease, student_log):
    logger.info(f"Starting feedback creation for scenario: {scenario_tracking_code}")
    
    # 1. تولید فیدبک از طریق هوش مصنوعی یا متد مربوطه
    try:
        feedback = generate_feedback(disease, type_disease, student_log)
    except Exception as e:
        logger.error(f"Error in feedback_generator: {str(e)}")
        return {"detail": "Error generating feedback content."}

    try:
        with transaction.atomic():
            # 2. پیدا کردن سناریو
            try:
                scenario = PulmonologyScenario.objects.select_for_update().get(tracking_code=scenario_tracking_code)
            except PulmonologyScenario.DoesNotExist:
                logger.warning(f"Scenario {scenario_tracking_code} not found.")
                return {"detail": "Scenario does not exist."}

            # 3. ثبت لاگ دانشجو (استفاده از defaults برای جلوگیری از جستجوی متنی سنگین)
            final_student_log_obj, created_log = StudentLog.objects.get_or_create(
                scenario=scenario,
                defaults={'student_log': student_log}
            )

            # 4. ثبت فیدبک
            final_feedback_obj, created_feedback = PulmonologyFeedback.objects.get_or_create(
                tracking_code=feedback_tracking_code,
                generated = True,
                defaults={
                    'feedback': feedback,
                    'scenario': scenario
                }
            )

            # 5. بروزرسانی وضعیت سناریو
            if not scenario.done:
                scenario.done = True
                scenario.save()
                logger.info(f"Scenario {scenario_tracking_code} marked as done.")

            logger.info(f"Feedback successfully created for code: {feedback_tracking_code}")
            return {"detail": "Feedback created successfully."}

    except Exception as e:
        logger.error(f"Database error in feedback_creator_celery: {str(e)}")
        return {"detail": f"An error occurred: {str(e)}"}