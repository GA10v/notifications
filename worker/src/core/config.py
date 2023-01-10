from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class FastapiSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8001
    NOTIFIC_PREFIX: str = '/app/v1/notification'

    class Config:
        env_prefix = 'FASTAPI_'


class RabbitMQSettings(BaseConfig):
    USER: str = 'guest'
    PASSWORD: str = 'guest'
    HOST: str = 'localhost'
    PORT: int = 5672
    QUEUES: list[str] = [
        'QUEUE_1',
    ]
    EXCHENGE_1: str = 'EXCHENGE_1'
    QUEUE_1: str = 'QUEUE_1'
    EXCHENGE_2: str = 'EXCHENGE_2'
    QUEUE_2: str = 'QUEUE_2'

    @property
    def uri(self):
        return f'amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'RABBIT_'


class SMTPSettings(BaseConfig):
    HOST: str = 'smtp.yandex.ru'
    PORT: int = 465
    USER: str
    PASSWODR: str

    class Config:
        env_prefix = 'SMTP_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Notification'
    BASE_DIR = Path(__file__).parent.parent
    rabbit: RabbitMQSettings = RabbitMQSettings()
    fastapi: FastapiSettings = FastapiSettings()
    smtp: SMTPSettings = SMTPSettings()


settings = ProjectSettings()
