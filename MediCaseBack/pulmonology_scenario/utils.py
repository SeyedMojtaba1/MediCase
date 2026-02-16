from celery import shared_task
from .scenario_creator import scenario_creator
from .feedback_utils.generate_feedback import generate_feedback
from .models import PulmonologyDisease, PulmonologyFeedback, UserScenarioAttempt, ScenarioTemplate, DailyScenario
from django.utils import timezone
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
            disease = PulmonologyDisease.objects.filter(
                english_name=target_disease_name, 
                type_disease=type_disease
            ).first()

            # اگر بیماری پیدا نشد، یکی جدید می‌سازیم
            if not disease:
                disease = PulmonologyDisease.objects.create(
                    english_name=target_disease_name, 
                    type_disease=type_disease
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
        print(f"❌ CRITICAL WORKER ERROR: {str(e)}") 
        import traceback
        traceback.print_exc()
        
        return {"detail": f"An internal error occurred: {str(e)}"}


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
            # اگر 'content' نبود کل دیکشنری رو به عنوان محتوا در نظر بگیر
            # یا حداقل یک دیکشنری خالی بده که دیتابیس خطا ندهد
            feedback_content = ai_response.get('content')
            if feedback_content is None:
                logger.warning(f"AI response dict didn't have 'content' key. Response: {ai_response}")
                feedback_content = ai_response # ذخیره کل جواب به عنوان فال‌بک
            
            score = ai_response.get('score')
        else:
            # اگر دیکشنری نبود (مثلا رشته بود)
            feedback_content = ai_response if ai_response else {}
            score = None

        # خط دفاعی آخر: اگر به هر دلیلی باز هم None بود
        if feedback_content is None:
            feedback_content = {"error": "AI response was empty or None"}

    except Exception as e:
        logger.error(f"Error in feedback_generator AI: {str(e)}")
        return {"detail": "Error generating feedback content."}

    try:
        with transaction.atomic():
            try:
                attempt = UserScenarioAttempt.objects.select_for_update().get(attempt_id=attempt_id)
            except UserScenarioAttempt.DoesNotExist:
                return {"detail": "User attempt record not found."}

            feedback_obj = PulmonologyFeedback.objects.create(
                attempt=attempt,
                feedback_content=feedback_content,
                generated=True,
                tracking_code=feedback_tracking_code
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

@shared_task
def generate_daily_scenarios_task():
    today = timezone.now().date()
    
    # بررسی می‌کنیم اگر برای امروز قبلا تولید شده، دوباره تولید نکند
    if DailyScenario.objects.filter(date=today).exists():
        return f"Daily scenarios for {today} already exist."

    generated_count = 0
    REQUIRED_COUNT = 20

    for _ in range(REQUIRED_COUNT):
        # 1. تولید دیتای سناریو
        case_data, disease_name_eng, type_disease = scenario_creator()
        
        # 2. پیدا کردن یا ساختن آبجکت بیماری (برای کلید خارجی)
        # فرض بر این است که نام بیماری در دیتابیس موجود است، اگر نباشد باید هندل شود
        disease_obj = PulmonologyDisease.objects.filter(english_name__iexact=disease_name_eng).first()
        
        if not disease_obj:
            # اگر بیماری پیدا نشد، لاگ می‌اندازیم و ادامه می‌دهیم (یا یک بیماری پیش‌فرض می‌سازیم)
            continue

        # 3. ساختن عنوان و ترکینگ کد
        tracking_code = str(uuid.uuid4())[:8].upper()
        title = f"سناریوی روزانه - {disease_obj.persian_name or disease_name_eng}"

        # 4. ذخیره در ScenarioTemplate
        template = ScenarioTemplate.objects.create(
            title=title,
            content=case_data,  # دیکشنری به صورت خودکار به JSON فیلد تبدیل می‌شود
            tracking_code=tracking_code,
            disease=disease_obj
        )

        # 5. لینک کردن به مدل DailyScenario برای امروز
        DailyScenario.objects.create(
            scenario_template=template,
            date=today
        )
        generated_count += 1

    return f"Successfully generated {generated_count} scenarios for {today}"