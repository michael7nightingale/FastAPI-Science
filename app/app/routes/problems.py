from fastapi import APIRouter, Request, Depends, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi_authtools import login_required

from app.db.repositories import ProblemRepository, ProblemMediaRepository, SolutionMediaRepository, SolutionRepository
from app.app.dependencies import get_repository, get_all_sciences


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

    print(problems)
    context = {
        "request": request,
        "problems": problems,
        "sciences": sciences,

    }
    return templates.TemplateResponse("problems.html", context)


@problems_router.get("/create")
@login_required
async def problem_create_get(request: Request, sciences: list = Depends(get_all_sciences)):
    context = {
        "request": request,
        "sciences": sciences,

    }
    return templates.TemplateResponse("problem_create.html", context)


@problems_router.post("/create")
@login_required
async def problem_create_post(
        request: Request,
        # ... Query()
        problems_repo: ProblemRepository = Depends(get_repository(ProblemRepository)),
        problems_media_repo: ProblemMediaRepository = Depends(get_repository(ProblemMediaRepository)),
):
    data = await request.form()
    await problems_repo.create(
        title=data['title'],
        text=data["text"],
        science_id=data['science'],
        user_id=request.user.id
    )
    return RedirectResponse(problems_router.url_path_for("problems_get"), status_code=303)


@problems_router.get('/detail/{problem_id}')
async def problem_get(
        request: Request,
        problem_id: str = Path(),
        problems_repo: ProblemRepository = Depends(get_repository(ProblemRepository)),
):
    problem, *problem_medias = await problems_repo.get_with_medias(problem_id)
    if problem is None:
        return {"detail": 404}
    context = {
        "request": request,
        "problem": problem,
        "problem_medias": problem_medias
    }
    return templates.TemplateResponse("problem.html", context)
