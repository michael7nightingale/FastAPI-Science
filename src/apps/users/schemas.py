from pydantic import BaseModel


class UserCustomModel(BaseModel):
    """Standard user request model."""
    id: str
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_authenticated: bool = True


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserRepresent(BaseModel):
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
