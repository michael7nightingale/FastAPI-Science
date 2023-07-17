from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase
from uuid import uuid4


class BaseAlchemyModel(DeclarativeBase):
    """May be useful"""
    pass


class TableMixin:
    """For getting dict object of the model."""
    id = Column(String(100), primary_key=True, default=lambda: str(uuid4()))

    def as_dict(self):
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}
