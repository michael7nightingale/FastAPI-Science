import json

from fastapi import APIRouter, Body, Request, Depends
from fastapi.responses import JSONResponse
from fastapi_authtools import login_required
from fastapi_authtools.exceptions import raise_invalid_credentials
from tortoise.exceptions import IntegrityError

import datetime
from .dependencies import get_oauth_provider
from .models import User
from src.services.oauth import Providers
from .schemas import UserRegister, UserCustomModel, UserLogin, ActivationScheme
from src.core.config import get_app_settings
from .tasks import send_activation_email_task


auth_router = APIRouter(prefix='/auth')


@auth_router.get('/{provider}/login')
async def provider_login(provider: Providers):
    """Login with Google."""
    return getattr(get_app_settings(), f"{provider.value}_login_url")


@auth_router.get("/{provider}/callback")
async def provider_callback(request: Request, code: str, provider=Depends(get_oauth_provider)):
    """Add access token from GitHub to cookies"""
    user_data = provider.provide()
    if user_data is None:
        return JSONResponse(
            {'detail': "Something went wrong."},
            status_code=500
        )
    try:
        user = await User.create(**user_data, active=True)
    except IntegrityError:
        user = await User.get(email=user_data['email'], username=user_data['username'])
    user_model = UserCustomModel(**user.as_dict())
    access_token = request.app.state.auth_manager.create_token(user_model)
    return {"access_token": access_token}


@auth_router.post('/token')
async def get_token(request: Request, user_token_data: UserLogin = Body()):
    """Token get view."""
    user = await User.login(
        **user_token_data.model_dump(exclude={"login"})
    )
    if user is None:
        raise_invalid_credentials()
    user_model = UserCustomModel(**user.as_dict())
    token = request.app.state.auth_manager.create_token(user_model)
    return {"access_token": token}


@auth_router.post("/register")
async def register(request: Request, user_data: UserRegister = Body()):
    """Registration POST view."""
    new_user = await User.register(**user_data.model_dump())
    if new_user is None:
        return JSONResponse(
            content={"detail": "Invalid data."},
            status_code=400,
        )
    send_activation_email_task.apply_async(
        kwargs={
            "name": new_user.username,
            "email": new_user.email
        }
    )
    return {"detail": f"Activation link is sent on email {new_user.email}. Please follow the instructions."}


@auth_router.get("/me")
@login_required
async def me(request: Request):
    return request.user


@auth_router.patch("/activation")
async def activate_user(
        request: Request,
        activation_scheme: ActivationScheme = Body()
):
    cache_code_value = await request.app.state.redis.get(f"code{activation_scheme.code}")
    if cache_code_value is None:
        return JSONResponse(
            content={"detail": "Код не найден."},
            status_code=400
        )
    cache_data = json.loads(cache_code_value)
    user = await User.get_or_none(email=cache_data['email'])
    exp_datetime = datetime.datetime.strptime(cache_data['exp'], "%d/%m/%y %H:%M:%S.%f")
    now_datetime = datetime.datetime.now()
    if now_datetime >= exp_datetime:
        send_activation_email_task.apply_async(
            kwargs={
                "name": user.username,
                "email": user.email
            }
        )
        return JSONResponse(
            content={"detail": "Срок действаия кода истек, выслали вам новый"},
            status_code=400
        )
    await user.activate()
    return {'detail': "Регистрация завершена успешно"}
