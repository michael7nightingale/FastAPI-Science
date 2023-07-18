from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi_authtools import login_required

from app.db.repositories import ProblemRepository, ProblemMediaRepository, SolutionMediaRepository, SolutionRepository
from app.api.dependencies import get_repository


problems_router = APIRouter(prefix="/problems")
templates = Jinja2Templates(directory="app/public/templates/problems/")


@problems_router.get("/")
async def problems_get(
        request: Request,
        problems_repo: ProblemRepository = Depends(get_repository(ProblemRepository))
):
    problems = await problems_repo.all_with_users()
    context = {
        "request": request,
        "problems": problems
    }
    return templates.TemplateResponse("problems.html", context)
