from fastapi import Form

from .schemas import UserRegister


async def get_user_register_data(
        username: str = Form(),
        email: str = Form(),
        password: str = Form()
):
    user_data = UserRegister(username=username, password=password, email=email)
    return user_data
