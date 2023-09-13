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


class PlotData(BaseModel):
    functions: list[str]
    x_min: int = Field(alias="xMin")
    x_max: int = Field(alias="xMax")
    y_min: int = Field(alias="yMin")
    y_max: int = Field(alias="yMax")

    @property
    def x_lim(self) -> tuple[int, int]:
        return self.x_min, self.x_max

    @property
    def y_lim(self) -> tuple[int, int]:
        return self.y_min, self.y_max


class EquationsData(BaseModel):
    equations: list[str]


class DownloadPlot(BaseModel):
    filename: str


class ScienceEnum(Enum):
    physics = "physics"
    mathem = "mathem"