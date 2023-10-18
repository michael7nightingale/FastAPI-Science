from enum import Enum

from .base import BaseProvider
from .google import GoogleOAuthProvider
from .github import GithubOAuthProvider
from .yandex import YandexOAuthProvider
from src.core.config import get_app_settings


class Providers(str, Enum):
    GITHUB = "github"
    GOOGLE = "google"
    YANDEX = "yandex"


def get_provider(provider_name: str, code: str) -> BaseProvider | None:
    settings = get_app_settings()
    match provider_name:
        case "google":
            return GoogleOAuthProvider(
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                client_id=settings.GOOGLE_CLIENT_ID,
                code=code
            )
        case "github":
            return GithubOAuthProvider(
                client_secret=settings.GITHUB_CLIENT_SECRET,
                client_id=settings.GITHUB_CLIENT_ID,
                code=code
            )
        case "yandex":
            return YandexOAuthProvider(
                client_secret=settings.YANDEX_CLIENT_SECRET,
                client_id=settings.YANDEX_CLIENT_ID,
                code=code
            )
        case _:
            return
