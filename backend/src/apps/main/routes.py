from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse


router = APIRouter(prefix='', tags=["Main"])


@router.get("/")
async def homepage(request: Request):
    """Main page."""
    return {"detail": "Application is started."}


@router.get("/github")
async def github_redirect(request: Request):
    """Redirect to the GitHub project repository."""
    return RedirectResponse(
        url="https://github.com/michael7nightingale/Calculations-FastAPI-Fullstack",
        status_code=303,
    )
