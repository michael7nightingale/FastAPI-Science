from pydantic import BaseModel, Field
from enum import Enum


class RequestSchema(BaseModel):
    data: dict | None = None
    url: str
    formula_id: str
    method: str = "GET"
    result: str | None = None
    find_mark: str = "x"
    user_id: str | int | None = None
    nums_comma: int = 10


class RequestData(BaseModel):
    data: dict | None = None
    find_mark: str = Field(default=10, alias="findMark")
    nums_comma: int = Field(default=10, alias="numsComma")


class DownloadPlot(BaseModel):
    filename: str


class ScienceEnum(Enum):
    physics = "physics"
    mathem = "mathem"
