from fastapi import Path, Request, Depends, HTTPException, Form

from app.db.repositories import (
    ProblemRepository,
    SolutionRepository,
    SolutionMediaRepository,
    ProblemMediaRepository
)

from app.app.dependencies import (
    get_problem_repository,
    get_solution_repository,
    get_problem_media_repository,
    get_solution_media_repository,

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
        problem_repo: ProblemRepository = Depends(get_problem_repository)
):
    problem = await problem_repo.get(problem_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Problem is not found."
        )
    return problem


async def get_problem_media(
        request: Request,
        problem_media_id: str = Path(),
        problem_media_repo: ProblemMediaRepository = Depends(get_problem_media_repository)
):
    problem = await problem_media_repo.get(problem_media_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Problem media is not found."
        )
    return problem


async def get_solution(
        request: Request,
        solution_id: str = Path(),
        solution_repo: SolutionRepository = Depends(get_solution_repository)
):
    problem = await solution_repo.get(solution_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Solution is not found."
        )
    return problem


async def get_solution_media(
        request: Request,
        solution_media_id: str = Path(),
        solution_media_repo: SolutionMediaRepository = Depends(get_solution_media_repository)
):
    problem = await solution_media_repo.get(solution_media_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Solution media is not found."
        )
    return problem

