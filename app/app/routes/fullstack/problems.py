from fastapi import APIRouter, Request, Depends, Path, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_authtools import login_required
from uuid import uuid4
from shutil import rmtree
import os

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
    get_solution_media_repository,
    get_problem,
    check_object_permissions,
    get_solution, get_problem_data, get_solution_data,
    get_solution_media, get_problem_media

)
from app.models.schemas import UserRepresent
from app.services.files import get_name_and_extension, get_all_request_files


problems_router = APIRouter(prefix="/problems")
templates = Jinja2Templates(directory='app/public/templates/problems/')


def problem_redirect(problem_id):
    return RedirectResponse(
        problems_router.url_path_for("problem_get", problem_id=problem_id), status_code=303
    )


@problems_router.get("/all")
async def problems_all(
        request: Request,
        sciences: list = Depends(get_all_sciences),
        problems_repo: ProblemRepository = Depends(get_problem_repository)
):
    """Endpoint for getting all problems."""
    if request.query_params:
        sciences_filters = []
        for k, v in request.query_params.items():
            if v == "on":
                sciences_filters.append(k)

        is_solved = bool(request.query_params.get("is_solved", False))
        problems = await problems_repo.filter_custom(sciences_filters, is_solved)

    else:
        problems = await problems_repo.all_with_users()
    for p in problems:
        p['user'] = UserRepresent(**p['user'].as_dict())
    context = {
        "request": request,
        "problems": problems,
        "sciences": sciences,
    }
    return templates.TemplateResponse("problems.html", context)


@problems_router.get("/create")
async def problem_create_get(
        request: Request,
        sciences=Depends(get_all_sciences)
):
    context = {
        "request": request,
        "sciences": sciences
    }
    return templates.TemplateResponse("problem_create.html", context)


media_extensions = {"png", "jpg", "img"}


@problems_router.post("/create")
@login_required
async def problem_create_post(
        request: Request,
        problem_data: dict = Depends(get_problem_data),
        problems_repo: ProblemRepository = Depends(get_problem_repository),
        problems_media_repo: ProblemMediaRepository = Depends(get_problem_media_repository),
):
    """Endpoint for creating problem."""
    problem = await problems_repo.create(
        **problem_data,
        user_id=request.user.id
    )
    problem_path = f"problems/{problem.id}/"
    problem_fullpath = os.path.join(request.app.state.STATIC_DIR, problem_path)
    os.makedirs(problem_fullpath)
    problem_medias_path = os.path.join(problem_path, "media")
    problem_medias_fullpath = os.path.join(request.app.state.STATIC_DIR, problem_medias_path)
    os.makedirs(problem_medias_fullpath)
    async for upload_file in get_all_request_files(request):
        problem_media_id = str(uuid4())
        _, ext = get_name_and_extension(upload_file.filename)
        if ext not in media_extensions:
            continue
        filename = f"{problem_media_id}.{ext}"
        problem_media_path = os.path.join(problem_medias_path, filename)
        problem_media_fullpath = os.path.join(request.app.state.STATIC_DIR, problem_media_path)
        await problems_media_repo.create(
            problem_id=problem.id,
            media_path=problem_media_path
        )
        with open(problem_media_fullpath, "wb") as file:
            file.write(await upload_file.read())

    return problem_redirect(problem.id)


@problems_router.get('/detail/{problem_id}')
async def problem_get(
        request: Request,
        problem_id: str = Path(),
        problems_repo: ProblemRepository = Depends(get_problem_repository),
        solutions_repo: SolutionRepository = Depends(get_solution_repository),
        solutions_media_repo: SolutionMediaRepository = Depends(get_solution_media_repository)
):
    problem, problem_medias = await problems_repo.get_with_medias(problem_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="There is not problem with such id."
        )
    solutions_ = await solutions_repo.get_with_users_by_problem_and_user(problem_id=problem_id,)
    solutions = []
    for s in solutions_:
        solutions.append(
            {
                "solution": s['solution'],
                "user": s['user'],
                "medias": await solutions_media_repo.filter(solution_id=s['solution'].id)
            }
        )

    my_solutions_ = await solutions_repo.get_with_users_by_problem_and_user(problem_id, request.user)
    my_solutions = []
    for s in my_solutions_:
        my_solutions.append(
            {
                                "solution": s['solution'],
                "user": s['user'],
                "medias": await solutions_media_repo.filter(solution_id=s['solution'].id)
            }
        )
    context = {
        "request": request,
        "problem": problem,
        "solutions": solutions,
        "my_solutions": my_solutions,
        "problem_medias": problem_medias,
    }

    return templates.TemplateResponse("problem.html", context)


@problems_router.delete('/detail/{problem_id}')
@login_required
async def problem_delete(
        request: Request,
        problem=Depends(get_problem),
        problems_repo: ProblemRepository = Depends(get_problem_repository),
):
    """Endpoint for deleting problem."""
    check_object_permissions(problem, request.user, "user_id")
    problem_fullpath = os.path.join(request.app.state.STATIC_DIR, problem.id)
    rmtree(problem_fullpath)
    await problems_repo.delete(problem.id)
    return


@problems_router.patch('/detail/{problem_id}')
@login_required
async def problem_update(
        request: Request,
        problem=Depends(get_problem),
        problem_data: dict = Depends(get_problem_data),
        problems_repo: ProblemRepository = Depends(get_problem_repository),
):
    """Endpoint for updating problem."""
    check_object_permissions(problem, request.user, "user_id")
    await problems_repo.update(problem.id, **problem_data)
    return problem_redirect(problem.id)


@problems_router.post('/detail/{problem_id}/solved')
@login_required
async def problem_solved(
        request: Request,
        problem=Depends(get_problem),
        solution=Depends(get_solution),
        problem_data: dict = Depends(get_problem_data),
        problems_repo: ProblemRepository = Depends(get_problem_repository),
):
    if solution.problem_id != problem.id:
        raise HTTPException(
            status_code=400,
            detail="Solution is not about the problem."
        )
    check_object_permissions(problem, request.user, "user_id")
    await problems_repo.set_solved(
        problem_id=problem.id,
        solution_id=solution.id
    )
    return problem_redirect(problem.id)


@problems_router.delete('/detail/{problem_id}/media/{problem_media_id}')
@login_required
async def problem_media_delete(
        request: Request,
        problem_media=Depends(get_problem_media),
        problem=Depends(get_problem),
        problem_media_repo: ProblemMediaRepository = Depends(get_problem_media_repository)
):
    """Endpoint for deleting problem media."""
    check_object_permissions(problem, request.user, "user_id")
    if problem_media.problem_id != problem.id:
        raise HTTPException(
            status_code=400,
            detail="Media is not about the problem."
        )
    problem_media_fullpath = os.path.join(
        request.app.state.STATIC_DIR, problem_media.media_path
    )
    os.remove(problem_media_fullpath)
    await problem_media_repo.delete(problem_media.id)
    return problem_redirect(problem.id)


@problems_router.post('/detail/{problem_id}/media')
@login_required
async def problem_media_add(
        request: Request,
        problem=Depends(get_problem),
        problem_media_repo: ProblemMediaRepository = Depends(get_problem_media_repository)
):
    """Endpoint for adding media files on the current problem."""
    check_object_permissions(problem, request.user, "user_id")
    problem_path = f"problems/{problem.id}"
    problem_medias_path = os.path.join(problem_path, "media")
    problem_medias_fullpath = os.path.join(request.app.state.STATIC_DIR, problem_medias_path)
    os.makedirs(problem_medias_fullpath)
    async for upload_file in get_all_request_files(request):
        problem_media_id = str(uuid4())
        _, ext = get_name_and_extension(upload_file.filename)
        filename = f"{problem_media_id}.{ext}"
        problem_media_path = os.path.join(problem_medias_path, filename)
        problem_media_fullpath = os.path.join(request.app.state.STATIC_DIR, problem_media_path)
        await problem_media_repo.create(
            problem_id=problem.id,
            media_path=problem_media_path
        )
        with open(problem_media_fullpath, "wb") as file:
            file.write(await upload_file.read())
    return problem_redirect(problem.id)


@problems_router.post('/detail/{problem_id}/solution')
@login_required
async def solution_create(
        request: Request,
        problem=Depends(get_problem),
        solution_data: dict = Depends(get_solution_data),
        solutions_repo: SolutionRepository = Depends(get_solution_repository),
        solution_medias_repo: SolutionMediaRepository = Depends(get_solution_media_repository)
):
    """Endpoint for creating solution on the current problem."""
    solution = await solutions_repo.create(
        **solution_data,
        problem_id=problem.id,
        author_id=request.user.id
    )
    data = await request.form()
    solution_path = f"problems/{problem.id}/{solution.id}/"
    solution_fullpath = os.path.join(request.app.state.STATIC_DIR, solution_path)
    os.makedirs(solution_fullpath)
    async for upload_file in get_all_request_files(request):
        solution_media_id = str(uuid4())
        _, ext = get_name_and_extension(upload_file.filename)
        filename = f"{solution_media_id}.{ext}"
        solution_media_path = os.path.join(solution_path, filename)
        solution_media_fullpath = os.path.join(request.app.state.STATIC_DIR, solution_media_path)
        await solution_medias_repo.create(
            solution_id=solution.id,
            media_path=solution_media_path
        )
        with open(solution_media_fullpath, "wb") as file:
            file.write(await upload_file.read())
    return problem_redirect(problem.id)


@problems_router.delete('/solutions/{solution_id}')
@login_required
async def solution_delete(
        request: Request,
        solution=Depends(get_solution),
        solution_repo: SolutionRepository = Depends(get_solution_repository)
):
    """Endpoint for deleting solution."""
    check_object_permissions(solution, request.user, "author_id")
    solution_fullpath = os.path.join(request.app.state.STATIC_DIR, "problems", solution.problem_id, solution.id)
    rmtree(solution_fullpath)
    await solution_repo.delete(solution.id)
    return problem_redirect(solution.problem_id)


@problems_router.patch('/solutions/{solution_id}')
@login_required
async def solution_update(
        request: Request,
        solution=Depends(get_solution),
        solution_data: dict = Depends(get_solution_data),
        solution_repo: SolutionRepository = Depends(get_solution_repository)
):
    """Endpoint for updating solution."""
    check_object_permissions(solution, request.user, "author_id")
    await solution_repo.update(solution.id, **solution_data)
    return problem_redirect(solution.problem_id)


@problems_router.delete('/solutions/{solution_id}/media/{solution_media_id}')
@login_required
async def solution_media_delete(
        request: Request,
        solution_media=Depends(get_solution_media),
        solution=Depends(get_solution),
        solution_media_repo: SolutionMediaRepository = Depends(get_solution_media_repository)
):
    """Endpoint for deleting solution media."""
    check_object_permissions(solution, request.user, "author_id")
    if solution_media.solution_id != solution.id:
        raise HTTPException(
            status_code=400,
            detail="Media is not about the solution."
        )
    solution_media_fullpath = os.path.join(
        request.app.state.STATIC_DIR, solution_media.media_path
    )
    os.remove(solution_media_fullpath)
    await solution_media_repo.delete(solution_media.id)
    return problem_redirect(solution.problem_id)


@problems_router.post('/solutions/{solution_id}/media')
@login_required
async def solution_media_add(
        request: Request,
        solution=Depends(get_solution),
        solution_medias_repo: SolutionMediaRepository = Depends(get_solution_media_repository)
):
    """Endpoint for adding media files on the current solution."""
    check_object_permissions(solution, request.user, "author_id")
    solution_path = f"problems/{solution.problerm_id}/{solution.id}/"
    solution_fullpath = os.path.join(request.app.state.STATIC_DIR, solution_path)
    os.makedirs(solution_fullpath)
    for upload_file in await get_all_request_files(request):
        solution_media_id = str(uuid4())
        _, ext = get_name_and_extension(upload_file.filename)
        filename = f"{solution_media_id}.{ext}"
        solution_media_path = os.path.join(solution_path, filename)
        solution_media_fullpath = os.path.join(request.app.state.STATIC_DIR, solution_media_path)
        await solution_medias_repo.create(
            solution_id=solution.id,
            media_path=solution_media_path
        )
        with open(solution_media_fullpath, "wb") as file:
            file.write(await upload_file.read())
    return problem_redirect(solution.problem_id)
