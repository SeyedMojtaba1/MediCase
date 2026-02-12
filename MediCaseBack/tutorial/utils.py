import base64
import uuid

def decode_short_uuid(short_uuid):
    try:
        padding = '=' * (-len(short_uuid) % 4)
        uuid_bytes = base64.urlsafe_b64decode(short_uuid + padding)
        return uuid.UUID(bytes=uuid_bytes)
    except Exception:
        raise ValueError("Invalid short UUID")