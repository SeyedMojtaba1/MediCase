from celery import shared_task
from .scenario_creator import scenario_creator
from .feedback_utils.generate_feedback import generate_feedback
from .models import PulmonologyDisease, PulmonologyFeedback, UserScenarioAttempt, ScenarioTemplate
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
import uuid, base64
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

def decode_short_uuid(short_id: str) -> uuid.UUID:
    padding = '=' * (-len(short_id) % 4)
    return uuid.UUID(bytes=base64.urlsafe_b64decode(short_id + padding))

@shared_task
def senario_creator_celery(personal_number, tracking_code):
    """
    وظیفه: تولید محتوای سناریو توسط هوش مصنوعی و ذخیره آن به عنوان یک Template.
    نکته: کسر اعتبار کاربر قبلاً در API انجام شده است.
    """
    logger.info(f"Starting scenario generation for tracking_code: {tracking_code}")

    # 1. فراخوانی هوش مصنوعی
    try:
        # خروجی فرضی: دیکشنری سناریو، نام انگلیسی بیماری، نوع بیماری
        scenario_data, target_disease_name, type_disease = scenario_creator()
        
        if isinstance(scenario_data, dict) and "error" in scenario_data:
            logger.error(f"AI Error: {scenario_data['error']}")
            return {"detail": scenario_data["error"]}
            
    except Exception as e:
        logger.error(f"AI Generation Failed: {str(e)}")
        return {"detail": "Error in AI generation."}

    try:
        with transaction.atomic():
            # 2. پیدا کردن یا ساختن بیماری (برای اطمینان از وجود آن)
            # استفاده از get_or_create برای جلوگیری از خطا اگر بیماری جدید بود
            disease, _ = PulmonologyDisease.objects.get_or_create(
                english_name=target_disease_name,
                defaults={
                    'type_disease': type_disease,
                    # 'persian_name': ... (اگر هوش مصنوعی برمی‌گرداند)
                }
            )

            # 3. ذخیره سناریو در جدول ScenarioTemplate
            # نکته: اینجا user دخالتی ندارد، چون این یک الگو است
            template, created = ScenarioTemplate.objects.get_or_create(
                tracking_code=tracking_code,
                defaults={
                    'title': f"Scenario for {target_disease_name}", # یا عنوانی که AI می‌دهد
                    'content': scenario_data,
                    'disease': disease
                }
            )

            if created:
                logger.info(f"ScenarioTemplate {tracking_code} created successfully.")
                return {"detail": "Scenario created successfully."}
            else:
                logger.warning(f"ScenarioTemplate {tracking_code} already exists.")
                return {"detail": "Scenario with this tracking code already exists."}

    except Exception as e:
        logger.error(f"Database error in senario_creator_celery: {str(e)}")
        return {"detail": "An internal error occurred."}


@shared_task
def feedback_creator_celery(feedback_tracking_code, attempt_id, disease_name, type_disease, student_log_data):
    """
    وظیفه: تولید فیدبک بر اساس لاگ دانشجو و اتصال آن به تلاش (Attempt) کاربر.
    ورودی: attempt_id جایگزین scenario_tracking_code شده است.
    """
    logger.info(f"Starting feedback creation for attempt_id: {attempt_id}")
    
    # 1. تولید فیدبک توسط هوش مصنوعی
    try:
        # فرض: هوش مصنوعی نمره (score) را هم برمی‌گرداند
        ai_response = generate_feedback(disease_name, type_disease, student_log_data)
        
        # مدیریت اینکه خروجی فقط متن است یا دیکشنری شامل نمره
        if isinstance(ai_response, dict):
            feedback_content = ai_response.get('content')
            score = ai_response.get('score') # ممکن است None باشد
        else:
            feedback_content = ai_response
            score = None

    except Exception as e:
        logger.error(f"Error in feedback_generator AI: {str(e)}")
        return {"detail": "Error generating feedback content."}

    try:
        with transaction.atomic():
            try:
                attempt = UserScenarioAttempt.objects.select_for_update().get(attempt_id=attempt_id)
            except UserScenarioAttempt.DoesNotExist:
                return {"detail": "User attempt record not found."}

            # ذخیره فیدبک: اضافه کردن tracking_code که در ورودی تابع آمده است
            feedback_obj = PulmonologyFeedback.objects.create(
                attempt=attempt,
                feedback_content=feedback_content,
                generated=True,
                tracking_code=feedback_tracking_code  # <--- این خط باید اضافه شود
            )

            if score is not None:
                attempt.score = score
            
            if not attempt.is_done:
                attempt.is_done = True
            
            attempt.save()

            logger.info(f"Feedback created successfully for attempt: {attempt_id}")
            return {"detail": "Feedback created successfully."}

    except Exception as e:
        logger.error(f"Database error in feedback_creator_celery: {str(e)}")
        return {"detail": f"An error occurred: {str(e)}"}