"""Module to store settings for url shortner."""
from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class DatabaseSettings(BaseConfig):
    PASSWORD: str = 'guest'
    USER: str = 'guest'
    DB: str = 'db_name'
    HOST: str = 'postgres'
    PORT: int | None = 5432

    @property
    def uri(self):
        return f'postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'

    class Config:
        env_prefix = 'POSTGRES_'


class URLShortnerSettings(BaseConfig):
    DEBUG: bool | None = True
    TESTING: bool | None = True


class ProjectSettings(BaseConfig):
    db: DatabaseSettings = DatabaseSettings()
    url_shortner: URLShortnerSettings = URLShortnerSettings()


settings = ProjectSettings()
