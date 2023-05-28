import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from starlette.templating import Jinja2Templates

from internal.users import get_current_user
from configuration.logger import logger


main_router = APIRouter(
    prefix=''
)
templates = Jinja2Templates(directory=os.getcwd() + '/public/templates/main/')

GITHUB_REDERECT_URL = "https://github.com/michael7nightingale/Calculations-FastAPI"


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


@main_router.get("/github/")
async def github_redirect(request: Request):
    return RedirectResponse(
        url=GITHUB_REDERECT_URL, 
        status_code=303,

    )