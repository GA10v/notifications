import uuid
from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class JWTSettings(BaseConfig):
    SECRET_KEY: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'TEST_JWT_'


class FastapiSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8000
    REVIEW_ENDPOINT: str = 'api/v1/notification/review'
    WELCOME_ENDPOINT: str = 'api/v1/notification/welcome'
    NEW_EPISODE_ENDPOINT: str = 'api/v1/notification/new_episode'
    GROUP_MESSAGE_ENDPOINT: str = 'api/v1/notification/group_message'

    @property
    def service_url(self):
        return f'http://{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'TEST_FASTAPI_'


class TestDataSettings(BaseConfig):
    USER: str = str(uuid.uuid4())
    EMAIL: str = 'user@mail.ru'
    LOGIN: str = 'user'
    CONTENT: str = str(uuid.uuid4())
    NOTIFICATION_1: str = str(uuid.uuid4())
    NOTIFICATION_2: str = str(uuid.uuid4())
    ART: str = 'series'
    EVENT: str = 'Вышла 8-я серия'
    USER_ROLE: str = 'sub'
    TEMPLATE_PATH: str = 'custom_mail_2023-01-10T21:52:40.441458.html'


class TestSettings(BaseConfig):
    PROJECT_NAME: str = 'Notification'
    BASE_DIR = Path(__file__).parent.parent
    jwt: JWTSettings = JWTSettings()
    fastapi: FastapiSettings = FastapiSettings()
    data: TestDataSettings = TestDataSettings()


settings = TestSettings()
