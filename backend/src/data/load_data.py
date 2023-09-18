from tortoise.exceptions import IntegrityError
import json
import csv

from src.apps.sciences.models import Science, Category, Formula


async def load_sciences() -> None:
    with open("src/data/files/sciences.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        try:
            await Science.create(**line)
        except IntegrityError:
            pass


async def load_categories() -> None:
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


async def load_formulas() -> None:
    with open("src/data/files/formulas.csv") as file:
        lines = list(csv.DictReader(file))

    for line in lines:
        try:
            await Formula.create(**line)
        except IntegrityError:
            pass


async def load_all_data() -> None:
    await load_sciences()
    await load_categories()
    await load_formulas()


async def load_formulas_mongo(db, collection_name) -> None:
    with open("src/data/files/formulas.json") as file:
        data = json.load(file)
    collection = getattr(db, collection_name)
    for d in data:
        obj = await collection.find_one({"slug": d['slug']})
        if obj is None:
            await collection.insert_one(d)


async def load_all_data_mongo(db) -> None:
    await load_formulas_mongo(db, "formulas")
