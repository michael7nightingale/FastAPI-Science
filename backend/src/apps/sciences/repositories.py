from src.base.repository import AsyncMongoRepository


class FormulaRepository(AsyncMongoRepository):
    collection_name = "formulas"
