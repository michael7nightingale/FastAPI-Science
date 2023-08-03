from fastapi import APIRouter, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.app.dependencies import get_user_register_data
from app.db.models import User
from app.models.schemas import UserRegister, UserCustomModel
from app.core.config import get_app_settings
from app.services.token import confirm_token, generate_activation_link


auth_router = APIRouter(
    prefix='/auth'
)
templates = Jinja2Templates('app/public/templates/auth/')


@auth_router.get('/github-login/')
async def github_login(request: Request):
    """Login with GitHub."""
    return RedirectResponse(get_app_settings().github_login_url, status_code=303)


@auth_router.get("/github-got")
async def github_get(request: Request, code: str):
    """Add access token from GitHub to cookies"""
    response = RedirectResponse(url='/', status_code=303)
    request.cookies['access-token'] = code
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
    print(user.describe())
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
