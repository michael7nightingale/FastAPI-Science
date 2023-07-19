import os

from pydantic_settings import BaseSettings
from socket import gethostbyname


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_driver: str
    db_host: str
    db_port: str
    db_name: str

    superuser_username: str
    superuser_password: str
    superuser_email: str

    algorithm: str
    secret_key: str
    expire_minutes: int

    github_redirect_url: str = "https://github.com/michael7nightingale/Calculations-FastAPI"
    github_client_id: str = "asdasd"

    @property
    def db_uri(self) -> str:
        host_address = gethostbyname(self.db_host)
        return f"{self.db_driver}://{self.db_user}:{self.db_password}@{host_address}:{self.db_port}/{self.db_name}"

    @property
    def github_login_url(self) -> str:
        return f"https://github.com/login/oauth/authorize?client_id={self.github_client_id}"

    class Config:
        if os.getenv("DOCKER"):
            env_file = ".docker.env"
        else:
            env_file = ".dev.env"


def get_app_settings() -> Settings:
    return Settings()
