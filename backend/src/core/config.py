from pydantic_settings import BaseSettings
import os


class BaseAppSettings(BaseSettings):
    SUPERUSER_USERNAME: str
    SUPERUSER_PASSWORD: str
    SUPERUSER_EMAIL: str

    ALGORITHM: str
    SECRET_KEY: str
    EXPIRE_MINUTES: int

    EMAIL_PORT: int
    EMAIL_HOST: str
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    REDIS_HOST: str
    REDIS_PORT: str

    MONGODB_URL: str
    MONGODB_NAME: str

    @property
    def CELERY_BROKER_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def github_login_url(self) -> str:
        return f"https://github.com/login/oauth/authorize?client_id={self.GITHUB_CLIENT_ID}"

    @property
    def google_login_url(self) -> str:
        return "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(  # noqa: E501
            token_request_uri="https://accounts.google.com/o/oauth2/auth",
            response_type="code",
            client_id=self.GOOGLE_CLIENT_ID,
            redirect_uri="http://localhost:8000/auth/google/callback",
            scope="https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        )


class DevSettings(BaseAppSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    @property
    def db_uri(self) -> str:
        host_address = self.DB_HOST
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{host_address}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        if os.getenv("DOCKER"):
            env_file = ".docker.env"
        else:
            env_file = ".dev.env"


def get_app_settings() -> BaseAppSettings:
    if os.getenv("TEST"):
        return TestSettings()
    else:
        return DevSettings()


class TestSettings(BaseAppSettings):
    DB_DRIVER: str
    DB_NAME: str

    github_redirect_url: str = "https://github.com/michael7nightingale/Calculations-FastAPI"
    github_client_id: str = "asdasd"

    @property
    def db_uri(self) -> str:
        return f"{self.DB_DRIVER}:///{self.DB_NAME}"

    class Config:
        env_file = ".test.env"


def get_test_app_settings() -> TestSettings:
    return TestSettings()
