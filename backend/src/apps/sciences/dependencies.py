from fastapi import Request, Depends, HTTPException
from .repositories import FormulaRepository

from .models import Science, Formula, Category


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


async def get_formula_dependency(formula_slug: str) -> Formula:
    formula = await Formula.get_or_none(slug=formula_slug)
    if formula is None:
        raise HTTPException(status_code=404, detail="Formula is not found.")
    return formula


async def get_science_dependency(science_slug: str) -> Science:
    science = await Science.get_or_none(slug=science_slug)
    if science is None:
        raise HTTPException(status_code=404, detail="Science is not found.")
    return science


async def get_category_dependency(category_slug: str) -> Category:
    category = await Formula.get_or_none(slug=category_slug)
    if category is None:
        raise HTTPException(status_code=404, detail="Category is not found.")
    return category
