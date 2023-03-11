"""Module to store settings for django admin panel."""
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


class DjangoSettings(BaseConfig):
    SECRET_KEY: str = 'sr2GPU6c5TxoEkqtnJCCNLPTs3ccyiwwBlETV2VmxfhUejVm9HlJhtHUIFANwjQbR'
    POSTGRES_PASSWORD: str = 'guest'
    POSTGRES_USER: str = 'guest'
    POSTGRES_DB: str = 'db_name'
    POSTGRES_HOST: str = 'postgres'
    POSTGRES_PORT: int | None = 5432
    ALLOWED_HOSTS: str | None = '127.0.0.1'
    DEBUG: bool = True

    @property
    def uri(self):
        return (
            f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    class Config:
        env_prefix = 'DJANGO_'


class ProjectSettings(BaseConfig):
    django: DjangoSettings = DjangoSettings()
    rabbit: RabbitMQSetting = RabbitMQSetting()


settings = ProjectSettings()
