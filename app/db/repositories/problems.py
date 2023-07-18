from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.repositories.base import BaseRepository
from app.db.models import Problem, SolutionMedia, ProblemMedia, Solution, User


class ProblemRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Problem, session)

    async def all_with_users(self):
        query = (
            select(self.model, User)
            .join(User, User.id == self.model.user_id)
        )
        result = (await self.session.execute(query).all())
        return [{"problem": i[0], "user": i[1]} for i in result]


class ProblemMediaRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(ProblemMedia, session)


class SolutionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Solution, session)


class SolutionMediaRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(SolutionMedia, session)
