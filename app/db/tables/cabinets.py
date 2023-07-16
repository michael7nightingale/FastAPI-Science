from sqlalchemy import Column, String, Integer

from app.db import Base
from app.db.tables.base import TableMixin


class History(Base, TableMixin):
    __tablename__ = 'history'

    formula = Column(String(40))
    result = Column(String(40))
    formula_url = Column(String(50))
    date_time = Column(String(40))
    user_id = Column(Integer)

    def history_view(self) -> str:
        return f"{self.formula} | {self.result} | {self.formula_url}"
