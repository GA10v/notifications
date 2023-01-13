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
    EXCHENGE_WELLCOME: str = 'EXCHENGE_1'
    QUEUE_WELLCOME: str = 'QUEUE_WELLCOME'
    EXCHENGE_REVIEW: str = 'EXCHENGE_REVIEW'
    QUEUE_REVIEW: str = 'QUEUE_REVIEW'
    EXCHENGE_EPISODE: str = 'EXCHENGE_EPISODE'
    QUEUE_EPISODE: str = 'QUEUE_EPISODE'
    EXCHENGE_MESSAGE: str = 'EXCHENGE_MESSAGE'
    QUEUE_MESSAGE: str = 'QUEUE_MESSAGE'

    @property
    def uri(self):
        return f'amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'RABBIT_'


class SMTPSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8025
    USER: str = 'LebASer'
    PASSWODR: str = 'vgqcfleohcdxcawk'

    class Config:
        env_prefix = 'SMTP_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Notification'
    BASE_DIR = Path(__file__).parent.parent
    rabbit: RabbitMQSettings = RabbitMQSettings()
    fastapi: FastapiSettings = FastapiSettings()
    smtp: SMTPSettings = SMTPSettings()


settings = ProjectSettings()
