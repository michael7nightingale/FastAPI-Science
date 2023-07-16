from sqlalchemy import Column, String, Text, Integer

from app.db import Base
from app.db.tables.base import TableMixin


class Science(Base, TableMixin):
    __tablename__ = 'sciences'

    title = Column(String(40), unique=True)
    content = Column(Text)
    slug = Column(String(40), unique=True)


class Category(Base, TableMixin):
    __tablename__ = 'categories'

    category_name = Column(String(40), unique=True)
    content = Column(Text)
    super_category = Column(String(40))
    slug = Column(String(40), unique=True)


class Formula(Base, TableMixin):
    __tablename__ = 'formulas'

    title = Column(String(40), unique=True)
    formula = Column(String(40))
    content = Column(Text)
    category_id = Column(Integer)
    slug = Column(String(40), unique=True)
