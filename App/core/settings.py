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
        db_url = URL.create(
            drivername="postgresql+asyncpg",
            database=self.name,
            port=self.port,
            host=self.host,
            username=self.user,
            password=self.password
        )
        return str(db_url)

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_prefix="DB_"
    )


class Config(BaseSettings):
    db: DBConfig = DBConfig()


config = Config()
