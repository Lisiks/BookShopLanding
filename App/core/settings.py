from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
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

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_prefix="APP_"
    )


class Config(BaseSettings):
    db: DBConfig = DBConfig()
    app: AppConfig = AppConfig()


config = Config()


