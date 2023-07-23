from datetime import datetime, timezone

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
    
    async def filter_custom(self, sciences: list = [], is_solved: bool = True):
        query = (
            select(self.model, User, Science)
            .join(User, User.id == self.model.user_id)
            .join(Science, Science.id == self.model.science_id)
            .where(self.model.is_solved == is_solved)
        )
        result = (await self.session.execute(query)).all()
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
                return None, []
            return problem, []
        else:
            problem = result[0][0]
            medias = [i[1] for i in result]
            return problem, medias

    async def set_solved(self, problem_id, solution_id) -> None:
        await self.update(
            problem_id,
            solve_solution_id=solution_id,
            is_solved=True,
            time_answered=datetime.now(tz=timezone.utc)
        )


class ProblemMediaRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(ProblemMedia, session)


class SolutionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Solution, session)

    async def get_with_users_by_problem_and_user(self, problem_id: str, user = None):
        query = (
            select(self.model, User)
            .join(User, User.id == self.model.author_id)
            .where(self.model.problem_id == problem_id)
        )
        if user is not None:
            query = query.where(self.model.author_id == user.id)
        result = (await self.session.execute(query)).all()
        return [
            {"user": r[1], "solution": r[0]} for r in result
        ]

    async def get_with_medias_by_problem(self, problem_id: str):
        query = (
            select(self.model, SolutionMedia)
            .join(SolutionMedia, SolutionMedia.solution_id == self.model.id)
            .where(self.model.problem_id == problem_id)
        )
        result = (await self.session.execute(query)).all()
        if not result:
            solutions = await self.filter(problem_id=problem_id)
            if not solutions:
                return [], []
            return solutions, []
        else:
            solutions = result[0][0]
            medias = [i[1] for i in result]
            return solutions, medias


class SolutionMediaRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(SolutionMedia, session)
