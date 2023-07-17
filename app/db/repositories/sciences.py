from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.base import BaseRepository, SlugGetMixin
from app.db.models import Science, Formula, Category


class ScienceRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Science, session)


class CategoryRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)


class FormulaRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Formula, session)
