from pydantic import BaseModel

from app.db.services.sqlalchemy_async import SQLAlchemyAsyncService
from app.db.models import User
from app.services.hash import verify_password, hash_password


class UserService(SQLAlchemyAsyncService):
    model = User

    async def login(self, username: str, password: str):
        user = await self.repository.get(username=username)
        if user is not None:
            if verify_password(password, user.password):
                return user

    async def register(self, user_data: dict | BaseModel):
        if isinstance(user_data, BaseModel):
            user_data = user_data.dict()

        user_data.update(password=hash_password(user_data['password']))
        new_user = await self.repository.create(**user_data)
        return new_user
