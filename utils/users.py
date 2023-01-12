import uuid
from abc import ABC, abstractmethod
from enum import Enum
from uuid import uuid4

import jwt
import requests
from pydantic import BaseModel
from faker import Faker
from requests import Session

from app.src.core.config import settings

fake = Faker()


class UserInfoSchema(BaseModel):
    user_id: uuid.UUID
    name: str
    last_name: str
    email: str
    phone_number: str
    gender: str
    country: str
    telegram_user_name: str
    time_zone: str


class UserRole(Enum):
    UNAUTHORIZED = 'unauth'
    SUBSCRIBERS = 'sub'
    MODERATORS = 'mod'
    ALL = 'all'


class UserInfoProtocol(ABC):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def get_user_info(self, user_id: str | None) -> UserInfoSchema:
        ...

    @abstractmethod
    def get_users_info(self, users_id: list[str | None]) -> list[UserInfoSchema]:
        ...

    @abstractmethod
    def get_users_info_by_role(self, user_role: UserRole) -> list[UserInfoSchema]:
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

    def get_user_info(self, user_id: str | None) -> UserInfoSchema:
        url = f'{self.base_url}/user-info'
        data = {'user_id': user_id}
        result = self.session.get(url=url, params=data, headers=self._headers())
        return result.json()

    def get_users_info(self, users_id: list[str | None]) -> list[UserInfoSchema]:
        ...

    def get_users_info_by_role(self, user_role: UserRole) -> list[UserInfoSchema]:
        ...


class FakeUserInfo(UserInfoProtocol):
    def connect(self):
        pass

    def get_user_info(self, user_id: str | None = None) -> UserInfoSchema:
        if not user_id:
            user_id = str(uuid4())

        return UserInfoSchema(
            user_id=user_id,
            name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            gender='male',
            country=fake.country(),
            telegram_user_name=f'@{fake.first_name()}',
            time_zone=fake.timezone(),
        )

    def get_users_info(self, users_id: list[str | None]) -> list[UserInfoSchema]:
        users = []
        for user_id in users_id:
            users.append(self.get_user_info(user_id=user_id))

        return users

    def get_users_info_by_role(self, user_role: UserRole) -> list[UserInfoSchema]:
        users_id = [str(uuid4()) for _ in range(20)]
        users = []
        for user_id in users_id:
            users.append(self.get_user_info(user_id=user_id))

        return users


def get_user_service() -> UserInfoProtocol:
    debug_service = True
    if debug_service:
        return FakeUserInfo()
    else:
        return UserInfo()
