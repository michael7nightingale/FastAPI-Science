from pydantic_settings import BaseSettings
from enum import StrEnum


class AppEnvTypes(StrEnum):
    prod = "prod"
    dev = "dev"
    test = "test"


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
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str

    REDIS_HOST: str
    REDIS_PORT: str

    MONGODB_URL: str
    MONGODB_NAME: str

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.REDIS_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.REDIS_URL

    @property
    def github_login_url(self) -> str:
        return f"https://github.com/login/oauth/authorize?client_id={self.GITHUB_CLIENT_ID}"

    @property
    def google_login_url(self) -> str:
        return "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(  # noqa: E501
            # noqa: E501
            token_request_uri="https://accounts.google.com/o/oauth2/auth",
            response_type="code",
            client_id=self.GOOGLE_CLIENT_ID,
            redirect_uri="http://localhost:8000/auth/google/callback",
            scope="https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        )

    @property
    def yandex_login_url(self) -> str:
        return "{token_request_uri}?response_type={response_type}&client_id={client_id}".format(
            token_request_uri="https://oauth.yandex.ru/authorize",
            response_type="code",
            client_id=self.YANDEX_CLIENT_ID,
        )

    class Config:
        env_file = ".env"
        app_env: AppEnvTypes = AppEnvTypes.dev
