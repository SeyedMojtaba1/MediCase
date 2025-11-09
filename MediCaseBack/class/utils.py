import uuid, base64

def decode_short_uuid(short_id: str) -> uuid.UUID:
    padding = '=' * (-len(short_id) % 4)
    return uuid.UUID(bytes=base64.urlsafe_b64decode(short_id + padding))

def encode_short_uuid(u):
    if isinstance(u, str):
        u = uuid.UUID(u)
    return base64.urlsafe_b64encode(u.bytes).rstrip(b'=').decode('ascii')