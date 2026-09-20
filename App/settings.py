from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, Field
from typing import Annotated
from sqlalchemy import URL


class DBConfig(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: str

    @computed_field
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_prefix="DB_"
    )


class AppConfig(BaseSettings):
    port: int
    reload: bool
    su_login: str
    su_password: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_prefix="APP_"
    )


class RedisConfig(BaseSettings):
    host: str
    port: int
    db: int

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_prefix="REDIS_"
    )


class SessionConfig(BaseSettings):
    ttl: int
    hash_key: str
    cookie_key: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_prefix="SESSION_"
    )


class PaginationConfig(BaseSettings):
    books_page_size: Annotated[int, Field(gt=0)]
    users_page_size: Annotated[int, Field(gt=0)]
    orders_page_size: Annotated[int, Field(gt=0)]
  

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_prefix="PAGINATION_"
    )


class Config(BaseSettings):
    db: DBConfig = DBConfig()
    app: AppConfig = AppConfig()
    pagination: PaginationConfig = PaginationConfig()
    redis: RedisConfig = RedisConfig()
    session: SessionConfig = SessionConfig()


config = Config()


