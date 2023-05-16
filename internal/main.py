import os
from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from internal.users import get_current_user
from configuration.logger import logger


main_router = APIRouter(
    prefix=''
)
templates = Jinja2Templates(directory=os.getcwd() + '/public/templates/main/')


# =================================== URLS ================================== #

@main_router.get("/")
async def homepage(request: Request):
    """Главная страница"""
    logger.info("Load main Page")
    context = {"request": request}
    user = await get_current_user(request)
    if user is not None:
        context.update(user=user)
    return templates.TemplateResponse("main.html", context=context)

