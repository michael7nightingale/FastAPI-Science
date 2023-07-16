from pydantic import BaseSettings
from socket import gethostbyname


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_driver: str
    db_host: str
    db_port: str
    db_name: str

    algorithm: str
    secret_key: str
    expire_minutes: int

    @property
    def db_uri(self) -> str:
        host_address = gethostbyname(self.db_host)
        return f"{self.db_driver}://{self.db_user}:{self.db_password}@{host_address}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".dev.env"


def get_app_settings() -> Settings:
    return Settings()
