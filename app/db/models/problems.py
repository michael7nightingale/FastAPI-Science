from sqlalchemy import Column, String, ForeignKey, DateTime,  func, Boolean, Text

from app.db import Base
from app.db.models.base import TableMixin


class Problem(TableMixin, Base):
    __tablename__ = "problems"

    title = Column(String(100))
    text = Column(Text)
    time_asked = Column(DateTime(timezone=True), server_default=func.now())
    time_answered = Column(DateTime(timezone=True), nullable=True)
    is_solved = Column(Boolean, default=False)
    solution_id = Column(String(100), ForeignKey("solutions.id", ondelete="SETNULL"), nullable=True)
    science_id = Column(String(100), ForeignKey("sciences.id", ondelete="CASCADE"))

    user_id = Column(String(100), ForeignKey("users.id"))


class Solution(TableMixin, Base):
    __tablename__ = "solutions"

    author_id = Column(String(100), ForeignKey("users.id", ondelete="CASCADE"))
    problem_id = Column(String(100), ForeignKey("problems.id", ondelete="CASCADE"))
    text = Column(Text)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class ProblemMedia(TableMixin, Base):
    __tablename__ = "problemmedias"

    problem_id = Column(String(100), ForeignKey("problems.id", ondelete="CASCADE"))
    media_path = Column(String(255))


class SolutionMedia(TableMixin, Base):
    __tablename__ = "solutionmedias"

    solution_id = Column(String(100), ForeignKey("solutions.id", ondelete="CASCADE"))
    media_path = Column(String(255))
