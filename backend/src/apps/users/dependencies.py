from fastapi import Form

from .oauth import Providers, get_provider, BaseProvider
from .schemas import UserRegister


async def get_user_register_data(
        username: str = Form(),
        email: str = Form(),
        password: str = Form()
):
    user_data = UserRegister(username=username, password=password, email=email)
    return user_data


async def get_oauth_provider(provider: Providers, code: str) -> BaseProvider:
    return get_provider(provider.value, code)
