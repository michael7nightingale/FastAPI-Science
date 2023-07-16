from sqlalchemy import String, Column
from uuid import uuid4


class TableMixin:
    """Base table mixin."""
    id = Column(String(100), primary_key=True, default=lambda: str(uuid4()))

    def as_dict(self) -> dict:
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}
