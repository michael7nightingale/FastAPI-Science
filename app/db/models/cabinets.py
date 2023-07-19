from sqlalchemy import Column, String, ForeignKey, func, DateTime

from app.db import Base
from app.db.models.base import TableMixin


class History(Base, TableMixin):
    __tablename__ = 'history'

    formula_id = Column(String(100), ForeignKey("formulas.id"))
    result = Column(String(100))
    formula_url = Column(String(50))
    date_time = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(String(100), ForeignKey("users.id"))

    def history_view(self) -> str:
        return f"{self.formula_id} | {self.result} | {self.formula_url}"
