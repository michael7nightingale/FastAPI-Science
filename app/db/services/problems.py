from app.db.services.sqlalchemy_async import SQLAlchemyAsyncService
from app.db.models import Problem, ProblemMedia, Solution, SolutionMedia, Science, User


class ProblemService(SQLAlchemyAsyncService):
    model = Problem

    async def all_with_users_and_sciences(self):
        return await self.repository.all_with_parents(
            {
                Science: "science_id",
                User: "user_id"
            }
        )

    async def filter_custom(self, sciences: list, is_solved: bool):
        results = await self.all_with_users_and_sciences()
        return [
            i for i in results if i['problem'].is_solved == is_solved and i['science'].slug in sciences
        ]

    async def get_with_medias(self, id_: str):
        return await self.repository.get_with_children(
            model=ProblemMedia,
            remote_field="problem_id",
            id=id_
        )

    async def set_solved(self, problem_id: str, solution_id):
        await self.update(problem_id, is_solved=True, solution_id=solution_id)


class ProblemMediaService(SQLAlchemyAsyncService):
    model = ProblemMedia


class SolutionService(SQLAlchemyAsyncService):
    model = Solution

    async def get_with_users_by_problem(self, problem_id: str):
        return await self.repository.filter_with_parents(
            models={
                User: "author_id",
            },
            problem_id=problem_id,
        )

    async def get_with_users_by_problem_and_user(self, problem_id: str, user_id: str):
        return await self.repository.filter_with_parents(
            models={
                User: "author_id",
            },
            problem_id=problem_id,
            author_id=user_id
        )


class SolutionMediaService(SQLAlchemyAsyncService):
    model = SolutionMedia
