from tortoise.exceptions import IntegrityError
import csv

from src.apps.sciences.models import Science, Category, Formula


async def load_sciences():
    with open("src/data/files/sciences.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        try:
            await Science.create(**line)
        except IntegrityError:
            pass


async def load_categories():
    with open("src/data/files/categories.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        try:
            if line['is_special'] is None:
                line['is_special'] = 0
            else:
                line['is_special'] = bool(int(line['is_special']))
            await Category.create(**line)
        except IntegrityError:
            pass


async def load_formulas():
    with open("src/data/files/formulas.csv") as file:
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
