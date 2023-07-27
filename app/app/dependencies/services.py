from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi import Depends, Request
from typing import Type, Callable

from app.db.services import (
    ScienceService,
    UserService,
    CategoryService,
    FormulaService,
    HistoryService,
    ProblemService,
    ProblemMediaService,
    SolutionService,
    SolutionMediaService,

)
from app.db.repositories.base import BaseRepository
from ...db.services.base import BaseService


def _get_pool(request: Request) -> async_sessionmaker:
    """Session maker pool is placed in fullstack`s state on fullstack`s startapp"""
    return request.app.state.pool


async def _get_session(pool=Depends(_get_pool)):
    """Save get and close the session"""
    async with pool() as session:
        yield session


def get_service(service_type: Type[BaseService]):
    """Get repository instance after getting the session."""
    def _get_repo(session=Depends(_get_session)) -> BaseRepository:
        return service_type(session)
    return _get_repo


def get_base_service(service_type: Type[BaseService]) -> Callable:
    """Repository dependency fabric function."""
    def inner(service: Type[BaseRepository] = Depends(get_service(service_type))):
        return service
    return inner


get_user_service = get_base_service(UserService)
get_science_service = get_base_service(ScienceService)
get_category_service = get_base_service(CategoryService)
get_history_service = get_base_service(HistoryService)
get_formula_service = get_base_service(FormulaService)
get_problem_service = get_base_service(ProblemService)
get_problem_media_service = get_base_service(ProblemMediaService)
get_solution_service = get_base_service(SolutionService)
get_solution_media_service = get_base_service(SolutionMediaService)
