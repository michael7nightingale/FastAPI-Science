from fastapi import Path, Request, Depends, HTTPException, Form

from app.db.services import (
    ProblemService,
    SolutionService,
    SolutionMediaService,
    ProblemMediaService
)

from app.app.dependencies.services import (
    get_problem_service,
    get_solution_service,
    get_problem_media_service,
    get_solution_media_service,

)


def get_problem_data(
        title: str = Form(),
        text: str = Form(),
        science: str = Form(),
):
    return {
        "text": text,
        "title": title,
        "science_id": science
    }


def get_solution_data(
        text: str = Form(),
):
    return {
        "text": text,
    }


async def get_problem(
        request: Request,
        problem_id: str = Path(),
        problem_service: ProblemService = Depends(get_problem_service)
):
    problem = await problem_service.get(problem_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Problem is not found."
        )
    return problem


async def get_problem_media(
        request: Request,
        problem_media_id: str = Path(),
        problem_media_service: ProblemMediaService = Depends(get_problem_media_service)
):
    problem = await problem_media_service.get(problem_media_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Problem media is not found."
        )
    return problem


async def get_solution(
        request: Request,
        solution_id: str = Path(),
        solution_service: SolutionService = Depends(get_solution_service)
):
    problem = await solution_service.get(solution_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Solution is not found."
        )
    return problem


async def get_solution_media(
        request: Request,
        solution_media_id: str = Path(),
        solution_media_service: SolutionMediaService = Depends(get_solution_media_service)
):
    problem = await solution_media_service.get(solution_media_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Solution media is not found."
        )
    return problem
