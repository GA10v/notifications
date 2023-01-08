from abc import ABC, abstractmethod
from uuid import uuid4

import jwt
import requests
from faker import Faker
from requests import Session

from app.src.core.config import settings

fake = Faker()


class UserInfoProtocol(ABC):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def get_user_info(self, user_id: str | None):
        ...


class UserInfo(UserInfoProtocol):
    def __init__(self, base_url: str = settings.auth.AUTH_URL) -> None:
        self.base_url = base_url
        self.session: Session = requests.Session()  # None

    def connect(self):
        if not self.session:
            self.session = requests.Session()

    @staticmethod
    def _headers() -> dict:
        _data = {
            'sub': str(uuid4()),
            'permissions': [0],
            'is_super': True,
        }
        access_token = jwt.encode(_data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)
        return {'Authorization': 'Bearer ' + access_token}

    def get_user_info(self, user_id: str | None):
        url = f'{self.base_url}/user-info'
        data = {'user_id': user_id}
        result = self.session.get(url=url, params=data, headers=self._headers())
        return result.json()


class FakeUserInfo(UserInfoProtocol):
    def connect(self):
        pass

    def get_user_info(self, user_id: str | None = None):
        if not user_id:
            user_id = str(uuid4())
        return {
            'user_info': {
                'user_id': user_id,
                'name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'phone_number': fake.phone_number(),
                'gender': 'male',
                'country': fake.country(),
                'telegram_user_name': f'@{fake.first_name()}',
                'time_zone': fake.timezone(),
            },
        }
