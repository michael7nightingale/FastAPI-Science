import os
from fastapi import APIRouter, Depends, Form, Path
from functools import lru_cache, wraps
from typing import Callable
from datetime import timedelta
from fastapi_login import LoginManager
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from package.exceptions import NotAuthenticatedException
from package.database import UsersDb as UDb, session, Users, HistoryDb as HDb
from package.schema import UserInSchema
from configuration.logger import logger


users_router = APIRouter(
    prefix='/accounts'
)
session = session()
UsersDb = UDb(session)
HistoryDb = HDb(session)
templates = Jinja2Templates(directory=os.getcwd() + '/public/templates/users/')


loginManager = LoginManager(
    'secret',
    token_url='/accounts/login',
    use_cookie=True,
    custom_exception=NotAuthenticatedException,
    default_expiry=timedelta(hours=12),

)


@loginManager.user_loader()
async def get_user_from_db(username: str):
    return await UsersDb.get_user(username)


async def get_current_user(request: Request) -> None | Users:
    token = request.cookies.get('access-token')
    if token is not None:
        try:
            user_dict = loginManager._get_payload(token)
            user = await get_user_from_db(username=user_dict['username'])
            logger.info(f"Got user with id: {user.id}!")
            # user = await UsersDb.get_user(user_dict['username'])
        except NotAuthenticatedException:
            user = None
        except:
            raise HTTPException(status_code=403, detail="You are not registered")
        return user


async def is_superuser(request: Request) -> Users | None:
    user = await get_current_user(request)
    if user:
        return user if user.is_superuser else None


async def is_stuff(request: Request) -> Users | None:
    user = await get_current_user(request)
    if user:
        return user if user.is_stuff else None


@lru_cache(maxsize=64)
def permission(permissions: tuple):
    __permissions = ('superuser', 'stuff')
    def decorator(func: Callable):
        @wraps(func)
        async def inner(request: Request, user, *args, **kwargs):
            nonlocal __permissions
            if not all(perm in __permissions for perm in permissions):
                raise HTTPException(status_code=403, detail='Permission denied')
            for i in set(permissions):
                if user is None:
                    if i == 'stuff':
                        user = await is_stuff(request)
                    elif i == 'superuser':
                        user = await is_superuser(request)
            if user is None:
                if permissions:
                    raise HTTPException(status_code=403, detail='Permission denied')
                else:
                    user = await get_current_user(request)
                    if user is None:
                        return RedirectResponse(url=users_router.url_path_for('login'), status_code=303)
            res = await func(request, user, *args, **kwargs)
            return res
        return inner
    return decorator


async def user_parameters(username: str = Form(),
                          password: str = Form()):
    return {"username": username,
            "password": password}


async def user_parameters_extra(parameters: dict = Depends(user_parameters),
                                email: str = Form()):
    parameters.update({"email": email})
    return parameters


# =================================== USERS ============================ #

@users_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse('login.html', context={"request": request,})


@users_router.post('/login')
async def login_post(request: Request,
                     user_data: dict = Depends(user_parameters)):
    user: Users = await UsersDb.login_user(user_data["username"],
                                           user_data['password'])
    user_access_token = loginManager.create_access_token(data=UserInSchema(**user.as_dict()).dict(),
                                                         expires=timedelta(hours=12))
    response = RedirectResponse(url="/", status_code=303)
    loginManager.set_cookie(response, user_access_token)
    request.state.user = user
    request.cookies['access-token'] = user_access_token
    return response


@users_router.get("/register")
async def register(request: Request,
                   user=None):
    return templates.TemplateResponse('register.html', context={"request": request,})


@users_router.post("/register")
async def register_post(request: Request,
                        user_data: dict = Depends(user_parameters_extra)):
    user = await UsersDb.create_user(**user_data)
    return RedirectResponse(users_router.url_path_for('login'), status_code=303)


@users_router.get('/logout')
async def logout(request: Request):
    response = RedirectResponse(url='/', status_code=303)
    response.delete_cookie(key='access-token')
    return response


@users_router.get('/{username}/')
@permission(permissions=())
async def cabinet(request: Request, user=None, username: str = Path()):
    if user.username == username:
        context = {'request': request,
                   "user": user}
        return templates.TemplateResponse("personal_cabinet.html", context=context)
    else:
        raise HTTPException(status_code=403)


@users_router.get('/history')
@permission(permissions=())
async def history(request: Request,
                  user=None,):
    history_list = await HistoryDb.get_history(user.id)
    context = {"title": "История вычислений",
               "history": history_list,
               "user": user,
               'request': request}
    return templates.TemplateResponse("history.html", context=context)
