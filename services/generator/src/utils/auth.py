from uuid import uuid4

from jose import jwt

from services.enricher.src.core.config import settings


def get_access_token() -> str:
    data = {
        'sub': str(uuid4()),
        'permissions': [0, 3],
        'is_super': True,
    }
    return jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)
