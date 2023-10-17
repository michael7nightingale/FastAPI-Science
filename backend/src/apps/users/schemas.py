from pydantic import BaseModel, EmailStr


class UserCustomModel(BaseModel):
    """Standard user request model."""
    id: str
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_authenticated: bool = True

    class Config:
        str_strip_whitespace = True


class UserRegister(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        str_strip_whitespace = True


class UserRepresent(BaseModel):
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        str_strip_whitespace = True


class UserLogin(BaseModel):
    login: str
    password: str
    email: EmailStr | None = None
    username: str | None = None

    def model_post_init(self, __context) -> None:
        if "@" in self.login:
            self.email = self.login
        else:
            self.username = self.login

    class Config:
        str_strip_whitespace = True
