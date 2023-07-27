from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import BaseAlchemyModel
from app.db.repositories.base import BaseRepository


class SQLAlchemyAsyncRepository(BaseRepository):
    """
    Repository class to access async sqlalchemy objects.
    """
    def __init__(self, model: type[BaseAlchemyModel], session: AsyncSession):
        self._model = model
        self._session = session

    @property
    def model(self):
        return self._model

    @property
    def session(self):
        return self._session

    async def create(self, **kwargs) -> BaseAlchemyModel | None:
        """Create new object in the table"""
        try:
            new_obj = self._model(
                **kwargs
            )
            await self.save(new_obj)
            return new_obj
        except IntegrityError:
            await self._session.rollback()
            return None

    async def get(self, *args, **kwargs) -> BaseAlchemyModel | None:
        """Get object by pk (id) or other."""
        if len(args) == 1:
            kwargs.update(id=args[0])
        elif len(args) > 1:
            raise ValueError("1 id arg expected.")
        expected = (
            getattr(self.model, key) == value for key, value in kwargs.items()
        )
        query = select(self._model).where(*expected)
        return (await self._session.execute(query)).scalar_one_or_none()

    async def filter(self, **kwargs) -> list[BaseAlchemyModel]:
        """Filter all objects by kwargs"""
        query = select(self._model).filter_by(**kwargs)
        return (await self._session.execute(query)).scalars().all()

    async def all(self) -> list[BaseAlchemyModel]:
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

    async def get_with_parents(self, models: dict, **kwargs):
        """Get object with several parents by FK."""
        query = select(self.model, *models)
        for model, local_field in models.items():
            query = query.join(model, model.id == getattr(self.model, local_field))
        expected = (
            getattr(self.model, key) == value for key, value in kwargs.items()
        )
        query = query.where(*expected)
        result = (await self.session.execute(query)).all()
        return result[0]

    async def all_with_parents(self, models: dict) -> list:
        """All objects with several parents by FK."""
        query = select(self.model, *models)
        for model, local_field in models.items():
            query = query.join(model, model.id == getattr(self.model, local_field))
        cur_result = (await self.session.execute(query)).all()
        models_ = [self.model] + list(models.keys())
        result = [
            {
                model.__name__.lower(): r[idx]
                for idx, model in enumerate(models_)
            }
            for r in cur_result
        ]
        return result

    async def filter_with_parents(self, models: dict, **kwargs) -> list:
        """Filter object with several parents by FK."""
        query = select(self.model, *models)
        for model, local_field in models.items():
            query = query.join(model, model.id == getattr(self.model, local_field))
        expected = (
            getattr(self.model, key) == value for key, value in kwargs.items()
        )
        query = query.filter(*expected)
        cur_result = (await self.session.execute(query)).all()
        models_ = [self.model] + list(models.keys())
        result = [
            {
                model.__name__.lower(): r[idx]
                for idx, model in enumerate(models_)
            }
            for r in cur_result
        ]
        return result

    async def get_with_children(self, model, remote_field: str, **kwargs):
        """Get object with children by FK."""
        expected = (
            getattr(self.model, key) == value for key, value in kwargs.items()
        )
        query = (
            select(self.model, model)
            .join(model, getattr(model, remote_field) == self.model.id)
            .where(*expected)
        )
        result = (await self.session.execute(query)).all()
        if not result:
            result = await self.get(**kwargs)
            if result is None:
                return None, None
            return result, []
        return result[0][0], [i[1] for i in result]

    async def commit(self):
        """Comfortably commit changes"""
        await self._session.commit()

    async def add(self, obj):
        """Comfortably add object"""
        self._session.add(obj)

    async def save(self, obj):
        await self.add(obj)
        await self.commit()
