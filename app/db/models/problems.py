from sqlalchemy import Column, String, ForeignKey, DateTime,  func, Boolean, Text

from app.db import Base
from app.db.models.base import TableMixin


class Problem(TableMixin, Base):
    __tablename__ = "problems"

    title = Column(String(100))
    text = Column(Text)
    time_asked = Column(DateTime(timezone=True), server_default=func.now())
    time_answered = Column(DateTime(timezone=True), nullable=True)
    is_closed = Column(Boolean, default=False)

    user_id = Column(String(100), ForeignKey("users.id"))


class Solution(TableMixin, Base):
    __tablename__ = "solutions"

    author_id = Column(String(100), ForeignKey("users.id"))
    problem_id = Column(String(100), ForeignKey("problems.id"))
    text = Column(Text)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class ProblemMedia(TableMixin, Base):
    __tablename__ = "problemmedias"

    problem_id = Column(String(100), ForeignKey("problems.id"))
    media_path = Column(String(255))


class SolutionMedia(TableMixin, Base):
    __tablename__ = "solutionmedias"

    solution_id = Column(String(100), ForeignKey("solutions.id"))
    media_path = Column(String(255))
