from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, select
from sqlalchemy.exc import IntegrityError
from typing import TypeVar

from app.db.models.base import BaseAlchemyModel


Model = TypeVar("Model", bound=BaseAlchemyModel)


class BaseRepository:
    """
    Base repository pattern class
    """
    def __init__(self, model: type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    async def create(self, **kwargs) -> Model | None:
        """Create new object in the table"""
        try:
            new_obj = self._model(
                **kwargs
            )
            await self.save(new_obj)
            return new_obj
        except IntegrityError:
            return None

    async def get(self, id_: int) -> Model | None:
        """Get object by pk (id)"""
        query = select(self._model).where(self._model.id == id_)
        return (await self._session.execute(query)).scalar_one_or_none()

    async def get_by(self, **kwargs) -> Model:
        """Filter all objects by kwargs"""
        query = select(self._model).filter_by(**kwargs)
        return (await self._session.execute(query)).scalar_one_or_none()

    async def filter(self, **kwargs) -> list[Model]:
        """Filter all objects by kwargs"""
        query = select(self._model).filter_by(**kwargs)
        return (await self._session.execute(query)).scalars().all()

    async def all(self) -> list[Model]:
        """Get all objects from the table"""
        query = select(self._model)
        return (await self._session.execute(query)).scalars().all()

    async def update(self, id_, **kwargs) -> None:
        """Update object by pk (id) with values kwargs"""
        query = update(self._model).where(self._model.id == id_).values(**kwargs)
        await self._session.execute(query)
        await self.commit()

    async def delete(self, id_) -> None:
        """Delete object by pk (id)"""
        query = delete(self._model).where(self._model.id == id_)
        await self._session.execute(query)
        await self.commit()

    async def clear(self) -> None:
        """Delete all objects from the table."""
        query = delete(self._model)
        await self._session.execute(query)
        await self.commit()

    async def commit(self):
        """Comfortably commit changes"""
        await self._session.commit()

    async def add(self, obj):
        """Comfortably add object"""
        self._session.add(obj)

    async def save(self, obj):
        await self.add(obj)
        await self.commit()


class SlugGetMixin:
    """
    Mixin for slug-getter can be useful
    """
    _session: AsyncSession
    _model: Model

    async def get(self, slug: str) -> Model | None:
        """Get on unique slug"""
        query = select(self._model).where(self._model.slug == slug)
        return (await self._session.execute(query)).scalar_one_or_none()
