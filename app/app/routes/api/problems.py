from fastapi import APIRouter, Request, Depends, Path
from fastapi_authtools import login_required

from app.db.repositories import (
    ProblemRepository,
    ProblemMediaRepository,
    SolutionMediaRepository,
    SolutionRepository,

)
from app.app.dependencies import (
    get_solution_repository,
    get_all_sciences,
    get_problem_repository,
    get_problem_media_repository,
    get_solution_media_repository
)


problems_router = APIRouter(prefix="/problems")


@problems_router.get("/")
async def problems_all(
        request: Request,
        sciences: list = Depends(get_all_sciences),
        problems_repo: ProblemRepository = Depends(get_problem_repository)
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

    return {
        "problems": problems,
        "sciences": sciences,
    }


@problems_router.post("/create")
@login_required
async def problem_create(
        request: Request,
        # ... Query()
        problems_repo: ProblemRepository = Depends(get_problem_repository),
        problems_media_repo: ProblemMediaRepository = Depends(get_problem_media_repository),
):
    data = await request.form()
    problem = await problems_repo.create(
        title=data['title'],
        text=data["text"],
        science_id=data['science'],
        user_id=request.user.id
    )
    return problem


@problems_router.get('/detail/{problem_id}')
async def problem_get(
        problem_id: str = Path(),
        problems_repo: ProblemRepository = Depends(get_problem_repository),
):
    problem, *problem_medias = await problems_repo.get_with_medias(problem_id)
    if problem is None:
        return {"detail": 404}
    return {
        "problem": problem,
        "problem_medias": problem_medias
    }
