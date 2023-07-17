from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
