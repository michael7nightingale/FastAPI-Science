from sqlalchemy import Column, String, Text, ForeignKey

from app.db import Base
from app.db.models.base import TableMixin


class Science(Base, TableMixin):
    __tablename__ = 'sciences'

    title = Column(String(40), unique=True)
    content = Column(Text)
    image_path = Column(String(100), nullable=True)
    slug = Column(String(40), unique=True, index=True)


class Category(Base, TableMixin):
    __tablename__ = 'categories'

    title = Column(String(40), unique=True)
    content = Column(Text)
    image_path = Column(String(100), nullable=True)
    science_id = Column(String(100), ForeignKey("sciences.id"))
    slug = Column(String(40), unique=True, index=True)


class Formula(Base, TableMixin):
    __tablename__ = 'formulas'

    title = Column(String(40), unique=True)
    formula = Column(String(40))
    content = Column(Text)
    image_path = Column(String(100), nullable=True)
    category_id = Column(String(100), ForeignKey("categories.id"))
    slug = Column(String(40), unique=True, index=True)
