from fastapi import APIRouter, Body, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi_authtools.models import UsernamePasswordToken
from fastapi_authtools.exceptions import raise_invalid_credentials

from app.app.dependencies import get_user_register_data
from app.app.dependencies import get_user_repository
from app.models.schemas import UserRegister, UserCustomModel
from app.db.repositories import UserRepository
from app.core.config import get_app_settings


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
async def get_token(
        request: Request,
        user_token_data: UsernamePasswordToken = Body(),
        user_repo: UserRepository = Depends(get_user_repository)
):
    """Token get view."""
    user = await user_repo.login(
        **user_token_data.dict()
    )
    print(user)
    if user is None:
        raise_invalid_credentials()
    user_model = UserCustomModel(**user.as_dict())
    token = request.app.state.auth_manager.create_token(user_model)
    return {"access_token": token}


@auth_router.post("/register")
async def register(
        user_data: UserRegister = Body(),
        user_repo: UserRepository = Depends(get_user_repository)
):
    """Registration POST view."""
    new_user = await user_repo.register(user_data)
    return new_user
