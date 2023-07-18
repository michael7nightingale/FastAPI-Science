from fastapi import APIRouter, Request, Depends, Path
from fastapi.templating import Jinja2Templates
from fastapi_authtools import login_required

from app.db.repositories import ProblemRepository, ProblemMediaRepository, SolutionMediaRepository, SolutionRepository
from app.api.dependencies import get_repository, get_all_sciences


problems_router = APIRouter(prefix="/problems")
templates = Jinja2Templates(directory="app/public/templates/problems/")


@problems_router.get("/")
async def problems_get(
        request: Request,
        sciences: list = Depends(get_all_sciences),
        problems_repo: ProblemRepository = Depends(get_repository(ProblemRepository))
):
    if request.query_params:
        sciences_filters = []
        for k, v in request.query_params.items():
            if v == "on":
                sciences_filters.append(k)

        is_closed = bool(request.query_params.get("is_closed", False))
        problems = await problems_repo.filter_custom(sciences_filters, is_closed)

    else:
        problems = await problems_repo.all_with_users()
    context = {
        "request": request,
        "problems": problems,
        "sciences": sciences,

    }
    return templates.TemplateResponse("problems.html", context)


@problems_router.post("/")
async def problems_post(
        request: Request,
        # ... Query()
        problems_repo: ProblemRepository = Depends(get_repository(ProblemRepository)),
        problems_media_repo: ProblemMediaRepository = Depends(get_repository(ProblemMediaRepository)),

):
    data = await request.form()
    ...


@problems_router.get('/{problem_id}')
async def problem_get(
        request: Request,
        problem_id: str = Path(),
        problems_repo: ProblemRepository = Depends(get_repository(ProblemRepository)),
):
    problem, problem_medias = await problems_repo.get(problem_id)
    if problem is None:
        return {"detail": 404}
    context = {
        "request": request,
        "problem": problem,
        "problem_medias": problem_medias
    }
    return templates.TemplateResponse("problem.html", context)
