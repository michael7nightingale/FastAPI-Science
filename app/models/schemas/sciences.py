from pydantic import BaseModel
from enum import Enum


class RequestSchema(BaseModel):
    data: dict
    url: str
    method: str = "GET"
    result: str | None = None
    find_mark: str = "x"
    user_id: str | None
    nums_comma: int = 10


class ScienceEnum(Enum):
    physics = "physics"
    mathem = "mathem"
