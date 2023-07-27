from app.db.services.sqlalchemy_async import SQLAlchemyAsyncService
from app.db.models import Science, Category, Formula


class ScienceService(SQLAlchemyAsyncService):
    model = Science

    async def get_with_categories(self, slug: str):
        return await self.repository.get_with_children(
            model=Category,
            remote_field="science_id",
            slug=slug
        )


class CategoryService(SQLAlchemyAsyncService):
    model = Category

    async def get_with_science(self, slug: str):
        return await self.repository.get_with_parents(
            models={
                Science: "science_id"
            },
            slug=slug
        )

    async def get_with_formulas(self, slug: str):
        return await self.repository.get_with_children(
            model=Formula,
            remote_field="category_id",
            slug=slug
        )


class FormulaService(SQLAlchemyAsyncService):
    model = Formula

    async def get_with_category(self, slug: str):
        return await self.repository.get_with_parents(
            models={
                Category: "category_id"
            },
            slug=slug
        )
