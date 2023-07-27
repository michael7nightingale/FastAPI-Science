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
        else:
            user_data = user_data.copy()
        user_data.update(password=hash_password(user_data['password']))
        new_user = await self.repository.create(**user_data)
        return new_user

    async def activate(self, user_id: str, email: str):
        user = await self.get(user_id)
        if user is not None and user.email == email:
            await self.update(user_id, is_active=True)
            return True
