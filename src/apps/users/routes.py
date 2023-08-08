from fastapi import APIRouter, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import requests

from .dependencies import get_user_register_data
from .models import User
from .schemas import UserRegister, UserCustomModel
from src.core.config import get_app_settings
from src.services.token import confirm_token, generate_activation_link


auth_router = APIRouter(
    prefix='/auth'
)
templates = Jinja2Templates('src/apps/users/templates/')


@auth_router.get('/github/login/')
async def github_login(request: Request):
    """Login with GitHub."""
    return RedirectResponse(get_app_settings().github_login_url, status_code=303)


@auth_router.get("/github/callback")
async def github_get(request: Request, code: str):
    """Add access token from GitHub to cookies"""
    settings = get_app_settings()
    response = RedirectResponse(url=request.app.url_path_for("homepage"), status_code=303)
    url = f"https://github.com/login/oauth/access_token?client_id={settings.GITHUB_CLIENT_ID}&client_secret={settings.GITHUB_CLIENT_SECRET}&code={code}"
    resp = requests.post(url)
    if not resp:
        return response
    resp_text = resp.text
    access_token = resp_text.split('=')[1].split("&")[0]
    headers = {"Authorization": f"Bearer {access_token}"}
    user_resp = requests.get("https://api.github.com/user", headers=headers)
    if not user_resp:
        return response
    user_data = user_resp.json()
    user_data['username'] = user_data['login']
    user_email_resp = requests.get("https://api.github.com/user/emails", headers=headers)
    if not user_email_resp:
        return response
    user_email_data = user_email_resp.json()
    email = None
    if isinstance(user_email_data, dict):
        email = user_email_data['email']
    else:
        for email_data in user_email_data:
            if email_data['primary']:
                email = email_data['email']
                break
        if email is None:
            email = email_data[0]['email']
    user_data['email'] = email
    user = UserCustomModel(**user_data)
    request.app.state.auth_manager.login(response, user)
    return response


@auth_router.get("/login")
async def login_get(request: Request):
    """Login GET view."""
    return templates.TemplateResponse('login.html', context={"request": request})


@auth_router.post('/login')
async def login_post(
        request: Request,
        username: str = Form(),
        password: str = Form(),
):
    """Login POST view."""
    user = await User.login(username, password)
    if user is None:
        return login_redirect()
    response = RedirectResponse("/", status_code=303)
    user_model = UserCustomModel(**user.as_dict())
    request.app.state.auth_manager.login(response, user_model)
    return response


def login_redirect():
    """Just a function to avoid writing redirect every time"""
    return RedirectResponse(auth_router.url_path_for("login_get"), status_code=303)


@auth_router.get("/register")
async def register_get(request: Request):
    """Registration GET view."""
    return templates.TemplateResponse('register.html', context={"request": request})


@auth_router.post("/register")
async def register_post(
        request: Request,
        user_data: UserRegister = Depends(get_user_register_data),
):
    """Registration POST view."""
    new_user = await User.register(**user_data.model_dump())
    if new_user is None:
        return RedirectResponse(auth_router.url_path_for("register_get"), status_code=303)
    # message = f"Activation link is sent on email {new_user.email}. Please follow the instructions."
    link = generate_activation_link(request, new_user)
    request.app.state.email_service.send_activation_email(
        name=new_user.username,
        link=link,
        email=new_user.email
    )
    return login_redirect()


@auth_router.get('/logout')
async def logout(request: Request):
    """Logout user view."""
    response = RedirectResponse(url=request.app.url_path_for('homepage'), status_code=303)
    request.app.state.auth_manager.logout(response)
    return response


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
                return login_redirect()
    return RedirectResponse(url=request.app.url_path_for('login_get'), status_code=303)
