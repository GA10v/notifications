from pathlib import Path

from pydantic import BaseSettings

from workers.src.core.config import RabbitMQSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class FastapiSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    NOTIFIC_PREFIX: str = '/api/v1/notification'

    class Config:
        env_prefix = 'FASTAPI_'


class PostgresSettings(BaseConfig):
    DB: str = 'db'
    USER: str = 'guest'
    PASSWORD: str = 'guest'
    HOST: str = 'localhost'
    PORT: int = 5432

    @property
    def uri(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    class Config:
        env_prefix = 'POSTGRES_'


class JWTSettings(BaseConfig):
    SECRET_KEY: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class AUTHSettings(BaseConfig):
    AUTH_URL: str = 'http://localhost/api/v1/user'

    class Config:
        env_prefix = 'AUTH_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Notification'
    BASE_DIR = Path(__file__).parent.parent
    rabbit: RabbitMQSettings = RabbitMQSettings()
    postgres: PostgresSettings = PostgresSettings()
    fastapi: FastapiSettings = FastapiSettings()
    jwt: JWTSettings = JWTSettings()
    auth: AUTHSettings = AUTHSettings()


settings = ProjectSettings()
