"""Config file to whole project."""
from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent.parent, 'env')
        env_file_encoding = 'utf-8'


class RabbitMQSetting(BaseConfig):
    USER: str = 'guest'
    PASSWORD: str = 'guest'
    HOST: str = 'localhost'
    PORT: int = 5672
    EXCHENGE_INCOMING_1: str = 'Exchange_incoming_1'
    EXCHENGE_INCOMING_2: str = 'Exchange_incoming_2'
    EXCHENGE_RETRY_1: str = 'Exchange_retry_1'
    EXCHENGE_RETRY_2: str = 'Exchange_retry_2'
    QUEUE_TO_ENRICH: str = 'Queue_to_enrich'
    QUEUE_TO_SEND: str = 'Queue_to_send'
    QUEUE_RETRY_ENRICH: str = 'Queue_retry_to_enrich'
    QUEUE_RETRY_SEND: str = 'Queue_retry_to_send'
    MESSAGE_TTL_MS: int = 10000

    @property
    def uri(self):
        return f'amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'RABBIT_'


class EmailSettings(BaseConfig):
    """Class is being used to keep all settings."""

    user: str
    password: str
    smtp_server: str
    smtp_port: int
    smtp_ssl: bool | None = True

    class Config:
        """Configuration plugin."""

        env_prefix = 'EMAIL_'


class PostgresSettings(BaseConfig):
    USER: str = 'guest'
    PASSWORD: str = 'guest'
    HOST: str = 'localhost'
    PORT: int = 5672
    DB: str = 'some_db'

    @property
    def uri(self):
        return f'://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'POSTGRES_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Notification_api'
    BASE_DIR = Path(__file__).parent.parent
    email: EmailSettings = EmailSettings()
    rabbit: RabbitMQSetting = RabbitMQSetting()
    postgres: PostgresSettings = PostgresSettings()


settings = ProjectSettings()
