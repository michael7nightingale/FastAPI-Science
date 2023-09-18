from fastapi import Request, Depends
from .repositories import FormulaRepository

from .models import Science


async def get_all_sciences():
    sciences = await Science.all()
    return sciences


async def get_mongodb_db(request: Request):
    return request.app.state.mongodb_db


def get_mongodb_repository(repository_class):
    def inner(db=Depends(get_mongodb_db)):
        return repository_class(db)
    return inner


get_formula_mongo_repository = get_mongodb_repository(FormulaRepository)
