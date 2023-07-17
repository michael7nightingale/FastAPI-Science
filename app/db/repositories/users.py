from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.repositories.base import BaseRepository
from app.db.models import User
from app.services.hash import hash_password, verify_password


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def login(self, username: str, password: str):
        user = await self.get_by(username=username)
        if user is not None:
            if verify_password(password, user.password):
                return user

    async def register(self, user_data: dict | BaseModel):
        if isinstance(user_data, BaseModel):
            user_data = user_data.dict()

        user_data.update(password=hash_password(user_data['password']))
        new_user = await self.create(**user_data)
        return new_user
