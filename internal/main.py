import os
from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from internal.users import get_current_user


main_router = APIRouter(
    prefix=''
)
templates = Jinja2Templates(directory=os.getcwd() + '/app/public/templates/main/')


# =================================== URLS ================================== #

@main_router.get("/")
async def homepage(request: Request):
    """Главная страница"""
    context = {"request": request}
    user = await get_current_user(request)
    if user is not None:
        context.update(user=user)
    return templates.TemplateResponse("main.html", context=context)

