from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


main_router = APIRouter(
    prefix=''
)
templates = Jinja2Templates('src/apps/main/templates/')


@main_router.get("/")
async def homepage(request: Request):
    """Main page."""
    context = {"request": request}
    return templates.TemplateResponse("main.html", context=context)


@main_router.get("/github/")
async def github_redirect(request: Request):
    """Redirect to the GitHub project repository."""
    return RedirectResponse(
        url="https://github.com/michael7nightingale/Calculations-FastAPI-Fullstack",
        status_code=303,
    )
