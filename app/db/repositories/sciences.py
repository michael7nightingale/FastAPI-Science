from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join


from app.db.repositories.base import BaseRepository, SlugGetMixin
from app.db.models import Science, Formula, Category


class ScienceRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Science, session)

    async def get_with_categories(self, slug: str):
        query = (
            select(self._model, Category)
            .join(Category, self._model.id == Category.science_id)
            .where(self._model.slug == slug)
        )
        result = (await self._session.execute(query)).all()
        science = result[0][0]
        categories = [i[1] for i in result]
        return science, categories


class CategoryRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)

    async def get_with_formulas(self, slug: str):
        query = (
            select(self._model, Formula)
            .join(Category, self._model.id == Formula.category_id)
            .where(self._model.slug == slug)
        )
        result = (await self._session.execute(query)).all()
        category = result[0][0]
        formulas = [i[1] for i in result]
        return category, formulas

    async def get_with_formulas_and_science(self, slug: str):
        query = (
            select(self._model, Science, Formula)
            .where(self._model.slug == slug)
            .join(Formula, self._model.id == Formula.category_id)
            .join(Science, Science.id == self._model.science_id)
            # .where(self._model.slug == slug)
        )
        result = (await self._session.execute(query)).all()
        if not result:
            return None
        category = result[0][0]
        science = result[0][1]
        formulas = [i[-1] for i in result]
        return category, science, formulas

    async def get_with_science(self, slug: str):
        query = (
            select(self.model, Science)
            .join(Science, Science.id == self.model.science_id)
            .where(self.model.slug == slug)
        )
        result = (await self.session.execute(query)).all()
        return result[0]


class FormulaRepository(SlugGetMixin, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Formula, session)

    async def get_with_category(self, slug: str):
        query = (
            select(self._model, Category)
            .join(Category, Category.id == self._model.category_id)
            .where(self._model.slug == slug)
        )
        result = (await self._session.execute(query)).all()
        return result[0]
