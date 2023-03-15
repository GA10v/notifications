from uuid import uuid4

import jwt

from admin_panel.core.config import settings


def get_access_token() -> str:
    data = {
        'sub': str(uuid4()),
        'permissions': [0, 3],
        'is_super': True,
    }
    return jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)
