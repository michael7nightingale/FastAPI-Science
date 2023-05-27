from enum import Enum
from pydantic import BaseModel, validator, Field
from datetime import datetime


class User(BaseModel):
    username: str = Field(min_length=5, max_length=40)
    email: str = Field(min_length=5, max_lenght=40)

    @classmethod
    @validator('email')
    def validate12(cls, value):
        if ' ' not in value.strip():
            data = value.strip().split("@")
            if len(data) == 2:
                if '.' in data[1] and not data[1].endswith('.'):
                    return value
        raise ValueError("Email is not correct")


class LoginUser(BaseModel):
     username: str = Field(min_length=5, max_length=40)
     password: str = Field(min_length=5, max_length=40)


class RegisterUser(LoginUser):
    email: str = Field(min_length=5, max_lenght=40)


class UserInDB(User):
    hashed_password: str = Field(min_length=5, max_length=40)
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
    user_id: int| None = None
    method: str
    url: str
    find_mark: str | None = None
    nums_comma: int | None = None
    data: dict | None = None




if __name__ == '__main__':
    user = UserSchema(
        username="michael",
        email='suslanchikmopl@gmail.com',
        password=''
    )

