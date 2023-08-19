from pydantic import BaseModel


class ProblemCreate(BaseModel):
    title: str
    text: str
    science_id: str


class ProblemUpdate(BaseModel):
    title: str | None = None
    text: str | None = None
    science: str | None = None


class SolutionCreate(BaseModel):
    text: str
