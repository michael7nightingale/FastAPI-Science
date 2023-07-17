from pydantic import BaseModel
from enum import Enum


class RequestSchema(BaseModel):
    data: dict
    user: object = None
    result: str | None = None


class ScienceEnum(Enum):
    physics = "physics"
    mathem = "mathem"
