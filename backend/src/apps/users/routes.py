from fastapi import APIRouter, Form, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from .dependencies import get_user_register_data, get_oauth_provider
from .models import User
from .oauth import Providers
from .schemas import UserRegister, UserCustomModel
from src.core.config import get_app_settings
from src.services.token import confirm_token, generate_activation_link
from ...base.apps import context_processor


auth_router = APIRouter(
    prefix='/auth'
)
templates = Jinja2Templates(
    directory='src/apps/users/templates/',
    context_processors=[context_processor]
)


@auth_router.get('/{provider}/login')
async def provider_login(provider: Providers):
    """Login with Google."""
    return RedirectResponse(getattr(get_app_settings(), f"{provider.value}_login_url"), status_code=303)


@auth_router.get("/{provider}/callback")
async def provider_callback(request: Request, code: str, provider=Depends(get_oauth_provider)):
    homepage_response = RedirectResponse(request.app.url_path_for("homepage"), status_code=303)
    login_response = RedirectResponse(auth_router.url_path_for("login_get"), status_code=303)
    user_data = provider.provide()
    if user_data is None:
        return login_response
    user = await User.get_or_none(email=user_data['email'])
    if user is None:
        await User.create(**user_data)
    user = UserCustomModel(**user_data)
    request.app.state.auth_manager.login(homepage_response, user)
    return homepage_response


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
        background_tasks: BackgroundTasks,
        user_data: UserRegister = Depends(get_user_register_data)
):
    """Registration POST view."""
    new_user = await User.register(**user_data.model_dump())
    if new_user is None:
        return RedirectResponse(auth_router.url_path_for("register_get"), status_code=303)
    # message = f"Activation link is sent on email {new_user.email}. Please follow the instructions."
    link = generate_activation_link(request, new_user)
    background_tasks.add_task(
        request.app.state.email_service.send_activation_email,
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
        email = confirm_token(token, secret_key=request.app.state.SECRET_KEY)
        if email is not None:
            if user.email == email:
                await User.activate(uuid)
                return login_redirect()
    return RedirectResponse(url=request.app.url_path_for('login_get'), status_code=303)
