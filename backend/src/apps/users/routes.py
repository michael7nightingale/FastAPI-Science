from fastapi import APIRouter, Body, Request, Depends
from fastapi.responses import JSONResponse
from fastapi_authtools import login_required
from fastapi_authtools.exceptions import raise_invalid_credentials
from tortoise.exceptions import IntegrityError

from .dependencies import get_oauth_provider
from .models import User, ActivationCode
from src.services.oauth import Providers
from .schemas import UserRegister, UserCustomModel, UserLogin, ActivationCodeScheme
from src.core.config import get_app_settings
from .tasks import send_email_task
from ...services.email import build_activation_email

router = APIRouter(prefix='/auth', tags=["Authentication"])


@router.get('/{provider}/login')
async def provider_login(provider: Providers):
    """Login with Google."""
    return getattr(get_app_settings(), f"{provider.value}_login_url")


@router.get("/{provider}/callback")
async def provider_callback_view(request: Request, code: str, provider=Depends(get_oauth_provider)):
    """Add access token from GitHub to cookies"""
    user_data = provider.provide()
    if user_data is None:
        return JSONResponse({'detail': "Something went wrong."}, status_code=500)
    try:
        user = await User.create(**user_data, active=True)
    except IntegrityError:
        user = await User.get(email=user_data['email'], username=user_data['username'])
    user_model = UserCustomModel(**user.as_dict())
    access_token = request.app.state.auth_manager.create_token(user_model)
    return {"access_token": access_token}


@router.post('/token')
async def get_token_view(request: Request, user_token_data: UserLogin = Body()):
    """Token get view."""
    user, password_correct = await User.login(
        **user_token_data.model_dump(exclude={"login"})
    )
    print(await User.all().values_list("email", flat=True))
    print(user_token_data.model_dump())
    print(123123, await User.get_or_none(email=user_token_data.login))
    if not user.is_active:
        activation_code = await ActivationCode.create_activation_code(user=user)
        send_email_task.apply_async(
            kwargs={
                "body": build_activation_email(activation_code),
                "to_addrs": [user.email],
                "subject": "Activation",
            }
        )
        return JSONResponse(
            {"detail": "Activation required check you email."},
            status_code=403
        )
    if not password_correct:
        return JSONResponse(
            {"detail": "Password is invalid."},
            status_code=400
        )
    user_model = UserCustomModel(**user.as_dict())
    token = request.app.state.auth_manager.create_token(user_model)
    return {"access_token": token}


@router.post("/register")
async def register_view(request: Request, user_data: UserRegister = Body()):
    """Registration POST view."""
    new_user = await User.register(**user_data.model_dump())
    if new_user is None:
        return JSONResponse({"detail": "Invalid data."}, status_code=400)
    activation_code = await ActivationCode.create_activation_code(user=new_user)
    send_email_task.apply_async(
        kwargs={
            "body": build_activation_email(activation_code),
            "to_addrs": [new_user.email],
            "subject": "Activation",
        }
    )
    return {"detail": f"Activation link is sent on email {new_user.email}. Please follow the instructions."}


@router.get("/me")
@login_required
async def me_view(request: Request):
    return request.user


@router.patch("/activation")
async def activate_user_view(
        request: Request,
        data: ActivationCodeScheme = Body()
):
    code = await ActivationCode.filter(**data.model_dump()).first().select_related("user")
    if code is None:
        return JSONResponse({"detail": False}, status_code=400)
    await code.user.activate()
    return {"detail": True}
