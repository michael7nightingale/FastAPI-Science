from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.repositories.base import BaseRepository
from app.db.models import Problem, SolutionMedia, ProblemMedia, Solution, User, Science


class ProblemRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Problem, session)

    async def all_with_users(self):
        query = (
            select(self.model, User, Science)
            .join(User, User.id == self.model.user_id)
            .join(Science, Science.id == self.model.science_id)
        )
        result = (await self.session.execute(query)).all()
        return [{"problem": i[0], "user": i[1], "science": i[2]} for i in result]
    
    async def filter_custom(self, sciences: list = [], is_closed: bool = True):
        query = (
            select(self.model, User, Science)
            .join(User, User.id == self.model.user_id)
            .join(Science, Science.id == self.model.science_id)
            .where(self.model.is_closed == is_closed)
        )
        result = (await self.session.execute(query)).all()
        print(result)
        print(sciences)
        return [{"problem": i[0], "user": i[1], "science": i[2]} for i in result if i[2].slug in sciences]

    async def get_with_medias(self, id_: str):
        query = (
            select(self.model, ProblemMedia)
            .join(ProblemMedia, ProblemMedia.problem_id == self.model.id)
            .where(self.model.id == id_)
        )
        result = (await self.session.execute(query)).all()
        if not result:
            problem = await self.get(id_)
            if problem is None:
                return [None]
            else:
                media_query = select(ProblemMedia)
                medias = (await self.session.execute(media_query)).scalars().all()
                return problem, medias
        else:
            problem = result[0][0]
            medias = [i[1] for i in result]
            return problem, medias


class ProblemMediaRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(ProblemMedia, session)


class SolutionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Solution, session)


class SolutionMediaRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(SolutionMedia, session)
