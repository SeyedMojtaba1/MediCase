import uuid, base64
from .models import Section
from datetime import date
from django.db.models import Q

def decode_short_uuid(short_id: str) -> uuid.UUID:
    padding = '=' * (-len(short_id) % 4)
    return uuid.UUID(bytes=base64.urlsafe_b64decode(short_id + padding))

def encode_short_uuid(u):
    if isinstance(u, str):
        u = uuid.UUID(u)
    return base64.urlsafe_b64encode(u.bytes).rstrip(b'=').decode('ascii')

def update_section_statuses():
    today = date.today()

    Section.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).exclude(status="Active").update(status="Active")

    Section.objects.filter(
        end_date__lt=today
    ).exclude(status="Finished").update(status="Finished")

    Section.objects.filter(
        start_date__gt=today
    ).exclude(status="Created").update(status="Created")