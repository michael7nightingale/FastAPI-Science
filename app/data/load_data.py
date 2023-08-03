from tortoise.exceptions import IntegrityError
import csv

from app.db.models import Science, Category, Formula


async def load_sciences():
    with open("app/data/files/sciences.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        try:
            await Science.create(**line)
        except IntegrityError:
            pass


async def load_categories():
    with open("app/data/files/categories.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        try:
            await Category.create(**line)
        except IntegrityError:
            pass


async def load_formulas():
    with open("app/data/files/formulas.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        try:
            await Formula.create(**line)
        except IntegrityError:
            pass


async def load_all_data():
    await load_sciences()
    await load_categories()
    await load_formulas()
