import os
from fastapi import APIRouter, Depends, Form, Path
from functools import lru_cache, wraps
from typing import Callable
from datetime import timedelta
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, FileResponse
from starlette.templating import Jinja2Templates

from app.formulas.exceptions import NotAuthenticatedException
from package import database
from package import schema
from configuration.logger import logger
from package import tables


users_router = APIRouter(
    prefix='/auth'
)
templates = Jinja2Templates(directory=os.getcwd() + '/public/templates/users/')

HISTORY_DIR = '/public/static/data/'


GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")

GITHUB_LOGIN_URL = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}"


# =================================== OAUTH ============================ #

@users_router.get('/github-login/')
async def github_login(request: Request):
    """Login with GitHub."""
    return RedirectResponse(GITHUB_LOGIN_URL, status_code=303)


@users_router.get("/github-got")
async def github_get(request: Request, code: str):
    """Add access token from GitHub to cookies"""
    response = RedirectResponse(url='/', status_code=303)
    # loginManager.set_cookie(response, token=code)
    # request.cookies['access-token'] = code

    return response


# =================================== USERS ============================ #

@users_router.get("/login")
async def login_get(request: Request):
    return templates.TemplateResponse('login.html', context={"request": request,})


@users_router.post('/login')
async def login_post(
        request: Request,
        user_schema: schema.LoginUser = Depends(user_login_parameters), 

    ):
    user: database.User = await UserDb.login_user(user_schema)
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
    """Just a function to avoid writing redirect every time"""
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
    """Logout user"""
    response = RedirectResponse(url='/', status_code=303)
    response.delete_cookie(key='access-token')
    return response


@users_router.get('/{username}/')
@permission(permissions=("user", ))
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
@permission(permissions=("user", ))
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
@permission(permissions=("user", ))
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
@permission(permissions=("user", ))
async def history_delete(
        request: Request,
        user=None
    ):
    await HistoryDb.delete_history(user.id)
    return RedirectResponse(url=users_router.url_path_for('history'), status_code=303)
