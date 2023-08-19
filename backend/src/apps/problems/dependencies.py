from fastapi import Path, Request, HTTPException, Form

from .models import Problem, ProblemMedia, Solution, SolutionMedia


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


async def get_problem(request: Request, problem_id: str = Path()):
    problem = await Problem.get_or_none(id=problem_id)
    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Problem is not found."
        )
    return problem


async def get_problem_media(request: Request, problem_media_id: str = Path()):
    problem_media = await ProblemMedia.get_or_none(id=problem_media_id)
    if problem_media is None:
        raise HTTPException(
            status_code=404,
            detail="Problem media is not found."
        )
    return problem_media


async def get_solution(
        request: Request,
        solution_id: str = Path(),
):
    solution = await Solution.get_or_none(id=solution_id)
    if solution is None:
        raise HTTPException(
            status_code=404,
            detail="Solution is not found."
        )
    return solution


async def get_solution_media(request: Request, solution_media_id: str = Path()):
    solution_media = await SolutionMedia.get_or_none(id=solution_media_id)
    if solution_media is None:
        raise HTTPException(
            status_code=404,
            detail="Solution media is not found."
        )
    return solution_media
