"""Config file to whole project."""

from pydantic import AmqpDsn, BaseSettings


class Settings(BaseSettings):
    """Class is being used to keep all settings."""

    email_user: str
    email_password: str
    email_smtp_server: str
    email_smtp_port: int
    email_smtp_ssl: bool | None = True
    rabbitmq_url: AmqpDsn
    rabbitmq_queue: str
    rabbitmq_exchange: str

    class Config:
        """Configuration plugin."""

        env_file = '.env'


settings = Settings()
