from pydantic_settings import BaseSettings
import os
from socket import gethostbyname


class BaseAppSettings(BaseSettings):
    SUPERUSER_USERNAME: str
    SUPERUSER_PASSWORD: str
    SUPERUSER_EMAIL: str

    ALGORITHM: str
    SECRET_KEY: str
    EXPIRE_MINUTES: int

    github_redirect_url: str = "https://github.com/michael7nightingale/Calculations-FastAPI"
    github_client_id: str = "asdasd"

    @property
    def github_login_url(self) -> str:
        return f"https://github.com/login/oauth/authorize?client_id={self.github_client_id}"


class DevSettings(BaseAppSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    @property
    def db_uri(self) -> str:
        host_address = gethostbyname(self.DB_HOST)
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{host_address}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        if os.getenv("DOCKER"):
            env_file = ".test.env"
        else:
            env_file = ".dev.env"


def get_app_settings() -> DevSettings:
    return DevSettings()


class TestSettings(BaseAppSettings):
    DB_DRIVER: str
    DB_NAME: str

    github_redirect_url: str = "https://github.com/michael7nightingale/Calculations-FastAPI"
    github_client_id: str = "asdasd"

    @property
    def db_uri(self) -> str:
        return f"{self.DB_DRIVER}:///{self.DB_NAME}"

    @property
    def github_login_url(self) -> str:
        return f"https://github.com/login/oauth/authorize?client_id={self.github_client_id}"

    class Config:
        env_file = ".test.env"


def get_test_app_settings() -> TestSettings:
    return TestSettings()
