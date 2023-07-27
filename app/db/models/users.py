from sqlalchemy import Column, String, Boolean

from app.db import Base
from app.db.models.base import TableMixin


class User(Base, TableMixin):
    __tablename__ = 'users'

    username = Column(String(40), unique=True)
    email = Column(String(40), unique=True)
    password = Column(String(100))
    last_login = Column(String(50))
    joined = Column(String(50))
    is_stuff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
