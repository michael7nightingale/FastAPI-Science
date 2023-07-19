from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker
import csv

from app.db.models import Science, Category, Formula


async def load_sciences(pool: async_sessionmaker):
    with open("app/data/files/sciences.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        async with pool() as session:
            try:
                science = Science(**line)
                session.add(science)
                await session.commit()
            except IntegrityError:
                pass


async def load_categories(pool: async_sessionmaker):
    with open("app/data/files/categories.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        async with pool() as session:
            try:
                science = Category(**line)
                session.add(science)
                await session.commit()
            except IntegrityError:
                pass


async def load_formulas(pool: async_sessionmaker):
    with open("app/data/files/formulas.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        async with pool() as session:
            try:
                science = Formula(**line)
                session.add(science)
                await session.commit()
            except IntegrityError:
                pass


async def load_all_data(pool: async_sessionmaker):
    await load_sciences(pool)
    await load_categories(pool)
    await load_formulas(pool)
