from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator
from datetime import datetime


class UserInSchema(BaseModel):
    username: str
    email: str

    @classmethod
    @validator('email')
    def validate12(cls, value):
        if ' ' not in value.strip():
            data = value.strip().split("@")
            if len(data) == 2:
                if '.' in data[1] and not data[1].endswith('.'):
                    return value
        raise ValueError("Email is not correct")


class UserSchema(UserInSchema):
    password: str
    last_login: datetime
    joined: datetime


class ScienceEnum(str, Enum):
    physics = 'physics'
    mathem = 'mathem'


class HistorySchema(BaseModel):
    user_id: int
    result: str
    formula: str
    formula_url: str
    date_time: str


class RequestSchema(BaseModel):
    user_id: Optional[int] = None
    method: str
    url: str
    find_mark: Optional[str] = None
    nums_comma: Optional[int] = None
    data: Optional[dict] = None




if __name__ == '__main__':
    user = UserSchema(
        username="michael",
        email='suslanchikmopl@gmail.com',
        password=''
    )

