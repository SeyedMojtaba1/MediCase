import uuid
import base64
import logging
from datetime import date
from django.db.models import Q
from .models import Section

logger = logging.getLogger('classroom')

def decode_short_uuid(short_id):
    if not short_id or not isinstance(short_id, str):
        logger.error(f"Failed to decode short UUID: input is {type(short_id)}")
        raise ValueError("شناسه کلاس نمی‌تواند خالی باشد.")

    try:
        padding = '=' * (-len(short_id) % 4)
        decoded_bytes = base64.urlsafe_b64decode(short_id + padding)
        
        return uuid.UUID(bytes=decoded_bytes)
    except Exception as e:
        logger.error(f"Failed to decode short UUID '{short_id}': {e}")
        raise ValueError("فرمت شناسه کلاس نامعتبر است.")

def encode_short_uuid(u):
    try:
        original_u = u
        if isinstance(u, str):
            u = uuid.UUID(u)
        result = base64.urlsafe_b64encode(u.bytes).rstrip(b'=').decode('ascii')
        logger.debug(f"Encoded UUID '{original_u}' to '{result}'")
        return result
    except Exception as e:
        logger.error(f"Failed to encode UUID '{u}': {e}", exc_info=True)
        raise e

def update_section_statuses():
    """
    Updates the status of Sections based on their start and end dates.
    Likely called by a periodic task (Celery/Cron).
    """
    try:
        today = date.today()
        logger.info(f"Starting scheduled task: update_section_statuses for date {today}")

        # 1. Update to 'Active'
        active_count = Section.objects.filter(
            start_date__lte=today,
            end_date__gte=today
        ).exclude(status="Active").update(status="Active")
        
        if active_count > 0:
            logger.info(f"Updated {active_count} sections to status 'Active'.")

        # 2. Update to 'Finished'
        finished_count = Section.objects.filter(
            end_date__lt=today
        ).exclude(status="Finished").update(status="Finished")

        if finished_count > 0:
            logger.info(f"Updated {finished_count} sections to status 'Finished'.")

        # 3. Update to 'Created' (Future sections)
        created_count = Section.objects.filter(
            start_date__gt=today
        ).exclude(status="Created").update(status="Created")

        if created_count > 0:
            logger.info(f"Updated {created_count} sections to status 'Created'.")

        total_updates = active_count + finished_count + created_count
        logger.info(f"Task update_section_statuses completed. Total records updated: {total_updates}")

    except Exception as e:
        logger.error(f"Critical error in update_section_statuses task: {e}", exc_info=True)
