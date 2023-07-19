from fastapi import Depends
from typing import Type, Callable

from .database import get_repository
from app.db.repositories import (
    UserRepository,
    ScienceRepository,
    CategoryRepository,
    FormulaRepository,
    ProblemRepository,
    ProblemMediaRepository,
    SolutionRepository,
    SolutionMediaRepository, HistoryRepository
)
from ...db.repositories.base import BaseRepository


def get_base_repository(repo_type: Type[BaseRepository]) -> Callable:
    """Repository dependency fabric function."""
    def inner(repo: Type[BaseRepository] = Depends(get_repository(repo_type))):
        return repo
    return inner


get_user_repository = get_base_repository(UserRepository)
get_science_repository = get_base_repository(ScienceRepository)
get_category_repository = get_base_repository(CategoryRepository)
get_history_repository = get_base_repository(HistoryRepository)
get_formula_repository = get_base_repository(FormulaRepository)
get_problem_repository = get_base_repository(ProblemRepository)
get_problem_media_repository = get_base_repository(ProblemMediaRepository)
get_solution_repository = get_base_repository(SolutionRepository)
get_solution_media_repository = get_base_repository(SolutionMediaRepository)
