from fastapi import APIRouter, Body, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi_authtools import login_required
from fastapi_authtools.models import UsernamePasswordToken
from fastapi_authtools.exceptions import raise_invalid_credentials

from app.db.models import User
from app.models.schemas import UserRegister, UserCustomModel
from app.core.config import get_app_settings
from app.services.token import confirm_token, generate_activation_link


auth_router = APIRouter(
    prefix='/auth'
)


@auth_router.get('/github-login/')
async def github_login():
    """Login with GitHub."""
    return RedirectResponse(get_app_settings().github_login_url, status_code=303)


@auth_router.get("/github-got")
async def github_get(code: str):
    """Add access token from GitHub to cookies"""
    return {"access_token": code}


@auth_router.post('/token')
async def get_token(request: Request, user_token_data: UsernamePasswordToken = Body()):
    """Token get view."""
    user = await User.login(
        **user_token_data.model_dump()
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
    link = generate_activation_link(request, new_user)
    request.app.state.email_service.send_activation_email(
        name=new_user.username,
        link=link,
        email=new_user.email
    )
    return {"detail":  f"Activation link is sent on email {new_user.email}. Please follow the instructions."}


@auth_router.get("/me")
@login_required
async def me(request: Request):
    return request.user


@auth_router.get("/activation/{uuid}/{token}")
async def activate_user(
        request: Request,
        uuid: str,
        token: str,
):
    user = await User.get_or_none(id=uuid)
    if user is not None:
        email = confirm_token(token)
        if email is not None:
            if user.email == email:
                await User.activate(uuid)
                return {"detail": "User is activated successfully."}
    return JSONResponse(
        content={"detail": "Activation link is invalid."},
        status_code=400
    )
