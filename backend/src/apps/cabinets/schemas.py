from datetime import datetime

from pydantic import BaseModel

from src.apps.sciences.schemas import FormulaListSchema, CategorySchema


class DownloadFile(BaseModel):
    filename: str
    extension: str


class HistoryListSchema(BaseModel):
    id: str
    result: float | str
    date_time: datetime
    formula: FormulaListSchema
    category: CategorySchema
