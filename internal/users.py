import os
from fastapi import APIRouter, Depends, Form, Path
from functools import lru_cache, wraps
from typing import Callable
from datetime import timedelta
from fastapi_login import LoginManager
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, FileResponse
from starlette.templating import Jinja2Templates

from package.exceptions import NotAuthenticatedException
from package import database
from package import schema
from configuration.logger import logger
from package import tables


users_router = APIRouter(
    prefix='/accounts'
)
session = database.session()
UserDb = database.UserDb(session)
HistoryDb = database.HistoryDb(session)
templates = Jinja2Templates(directory=os.getcwd() + '/public/templates/users/')

HISTORY_DIR = '/public/static/data/'

loginManager = LoginManager(
    'secret',
    token_url='/accounts/login',
    use_cookie=True,
    custom_exception=NotAuthenticatedException,
    default_expiry=timedelta(hours=12),

)


@loginManager.user_loader()
async def get_user_from_db(username: str):
    return await UserDb.get_user(username)


async def get_current_user(request: Request) -> database.User:
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


async def is_superuser(request: Request):
    user = await get_current_user(request)
    if user:
        return user if user.is_superuser else None


async def is_stuff(request: Request):
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


async def user_login_parameters(
        request: Request, 
        #username: str = Form(default=""),
        #password: str = Form(default=""), 

    ) -> schema.LoginUser:
    form_data = await request.form()
    print(form_data)
    return schema.LoginUser(**form_data)
    #return schema.LoginUser(username=username, password=password)


async def user_register_parameters(
        request: Request,
        #parameters: dict = Depends(user_login_parameters),
        #email: str = Form()
    ) -> schema.RegisterUser:
    form_data = await request.form()
    print(form_data)
    return schema.RegisterUser(**form_data)
    #parameters.update({"email": email})
    #return parameters


# =================================== USERS ============================ #

@users_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse('login.html', context={"request": request,})


@users_router.post('/login')
async def login_post(
        request: Request,
        user_schema: schema.LoginUser = Depends(user_login_parameters), 

    ):
    user: database.Users = await UserDb.login_user(user_schema)
    if user is not None:
        user_access_token = loginManager.create_access_token(
            data=user.as_dict(),
            expires=timedelta(hours=12)
        )
        response = RedirectResponse(url="/", status_code=303)
        loginManager.set_cookie(response, user_access_token)
        request.state.user = user
        request.cookies['access-token'] = user_access_token
        return response
    return login_redirect()


def login_redirect():
     return RedirectResponse(users_router.url_path_for("login"), status_code=303)


@users_router.get("/register")
async def register(
        request: Request,

    ):
    return templates.TemplateResponse('register.html', context={"request": request,})


@users_router.post("/register")
async def register_post(
        request: Request,
        user_schema: schema.RegisterUser = Depends(user_register_parameters)
    ):
    user = await UserDb.create_user(user_schema)
    return login_redirect()


@users_router.get('/logout')
async def logout(request: Request):
    response = RedirectResponse(url='/', status_code=303)
    response.delete_cookie(key='access-token')
    return response


@users_router.get('/{username}/')
@permission(permissions=())
async def cabinet(
        request: Request,
        user=None,
        username: str = Path()
    ):
    if user.username == username:
        context = {
            'request': request,
            "user": user
        }
        return templates.TemplateResponse("personal_cabinet.html", context=context)
    else:
        raise HTTPException(status_code=403, detail='Unauthorized.')


@users_router.get('/history')
@permission(permissions=())
async def history(request: Request,
                  user=None,):
    delete_history_csv(user.id)
    history_list = await HistoryDb.get_history(user.id)
    context = {
        "title": "История вычислений",
        "history": history_list,
        "user": user,
        'request': request
    }
    return templates.TemplateResponse("history.html", context=context)


@users_router.post('/download_history')
@permission(permissions=())
async def history_download(
        request: Request,
        user=None,
        filename: str = Form()
    ):
    history_list = await HistoryDb.get_history(user.id)
    filepath = os.getcwd() + HISTORY_DIR + f'{user.id}.csv'
    table = tables.CsvTableManager(filepath)
    history_list = [i.as_dict() for i in history_list]

    if history_list:
        table.init_data(history_list[0].keys())
        for line in history_list:
            table.add_line(line.values())
        table.save_data(filepath)
        return FileResponse(path=filepath, filename=f"{filename}.csv")
    else:
        return RedirectResponse(url=users_router.url_path_for('history'), status_code=303)


def delete_history_csv(user_id: int):
    """Удаление файла .csv с историей вычислений"""
    path = os.getcwd() + HISTORY_DIR + f'{user_id}.csv'
    if os.path.exists(path):
        os.remove(path)
    else:
        return None


@users_router.post('/delete_history')
@permission(permissions=())
async def history_delete(
        request: Request,
        user=None
    ):
    await HistoryDb.delete_history(user.id)
    return RedirectResponse(url=users_router.url_path_for('history'), status_code=303)
