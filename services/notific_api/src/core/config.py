from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)


class BaseConfig(BaseSettings):
    class Config:
        # env_file = Path(Path(__file__).parent.parent.parent.parent.parent, 'env')
        env_file_encoding = 'utf-8'


class FastapiSetting(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8080
    NOTIFIC_PREFIX: str = '/api/v1/notification'

    class Config:
        env_prefix = 'FASTAPI_'


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


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'Notifications API'
    BASE_DIR = Path(__file__).parent.parent
    fastapi: FastapiSetting = FastapiSetting()
    rabbit: RabbitMQSetting = RabbitMQSetting()


settings = ProjectSettings()
