from pydantic import BaseModel


class SolutionCreate(BaseModel):
    text: str
