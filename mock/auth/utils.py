import re
from datetime import datetime
from random import choice
from typing import Optional
from uuid import uuid4

import jwt
from config import settings
from faker import Faker
from jwt import DecodeError, ExpiredSignatureError
from models import DeliveryType, NewUserInfo, UserInfo, WelcomeEvent
from requests import post

fake = Faker()


def _parse_auth_header(
    auth_header: str,
    access_token_title: str = 'Bearer',
    refresh_token_title: str = 'Refresh',
) -> dict:
    """Parses a Authorization/Authentication http header and extracts the access + request
    tokens if present.
    Example header:
    "Authorization: Bearer AAA, Refresh BBB"
    """

    def _match_token(token_title: str) -> Optional[str]:
        expression = re.escape(token_title) + r' ([^\s,]+)'
        match = re.search(expression, auth_header)
        try:
            return match.group(1)
        except (AttributeError, IndexError):
            return None

    return {'access_token': _match_token(access_token_title), 'refresh_token': _match_token(refresh_token_title)}


def parse_header(auth_header) -> dict:
    jwt_token = _parse_auth_header(auth_header)['access_token']
    try:
        decoded_jwt = jwt.decode(jwt=jwt_token, key=settings.jwt.SECRET_KEY, algorithms=[settings.jwt.ALGORITHM])
        return {
            'user_id': decoded_jwt.identity,
            'claims': decoded_jwt.additional_claims,
        }
    except (DecodeError, ExpiredSignatureError):
        ...  # TODO Добавить логгер


def get_new_user() -> NewUserInfo:
    return NewUserInfo(
        user_id=str(uuid4()),
        name=fake.first_name(),
        email=fake.email(),
    )


def get_fake_user(user_id: str | None = None) -> UserInfo:
    if not user_id:
        user_id = uuid4()

    return UserInfo(
        user_id=str(user_id),
        name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=str(fake.phone_number()),
        gender=choice(['male', 'female']),
        country=fake.country(),
        telegram_name=f'@{fake.first_name()}',
        time_zone=fake.timezone(),
        birthday=fake.date(),
        delivery_type=[
            DeliveryType.email,
        ],
    )


def get_fake_users(users_id: list[str] | None = None) -> list[UserInfo]:
    users = []
    if users_id:
        for user_id in users_id:
            users.append(get_fake_user(user_id))
        return users

    users_id = [str(uuid4()) for _ in range(20)]
    for user_id in users_id:
        users.append(get_fake_user(user_id))
    return users


def get_fake_group() -> list[str]:
    return [str(uuid4()) for _ in range(20)]


def _headers() -> str:
    data = {
        'sub': str(uuid4()),
        'permissions': [0, 3],
        'is_super': True,
    }
    access_token = jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)
    return {'Authorization': 'Bearer ' + access_token}


def create_event() -> None:
    # TODO добавить путь к API_Notific
    url = f'http://{settings.notific.HOST}:{settings.notific.PORT}{settings.notific.NOTIFIC_PREFIX}/send'
    headers = _headers()
    params = WelcomeEvent(
        source_name='Auth',
        event_type='welcome_message',
        delivery_type=DeliveryType.email,
        context=get_new_user().dict(),
        created_at=datetime.now(),
    ).dict()
    post(url=url, headers=headers, params=params)
