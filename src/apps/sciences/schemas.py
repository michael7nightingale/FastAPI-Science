from pydantic import BaseModel
from enum import Enum


class RequestSchema(BaseModel):
    data: dict | None = None
    url: str
    formula_id: str
    method: str = "GET"
    result: str | None = None
    find_mark: str = "x"
    user_id: str | None = None
    nums_comma: int = 10


class RequestData(BaseModel):
    data: dict | None = None
    find_mark: str = "x"
    nums_comma: int = 10


class ScienceEnum(Enum):
    physics = "physics"
    mathem = "mathem"
