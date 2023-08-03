from tortoise import fields

from app.db.models.base import TortoiseModel


class Problem(TortoiseModel):
    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=255)
    text = fields.TextField()
    user = fields.ForeignKeyField("models.User", related_name="problems")
    # solution = fields.OneToOneField("models.Solution", related_name="problem_solved", null=True)
    science = fields.ForeignKeyField("models.Science", related_name="problems")
    is_solved = fields.BooleanField(default=False)
    time_opened = fields.DatetimeField(auto_now=True)
    time_solved = fields.DatetimeField(null=True)

    @classmethod
    async def all(cls, using_db=None):
        return await (
            super()
            .all(using_db)
            .prefetch_related("medias")
            .select_related("science", "user")
        )

    @classmethod
    async def get_or_none(cls, *args, using_db=None, **kwargs):
        return await (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .prefetch_related("medias", "solutions")
            .select_related("science", "user")
        )


class ProblemMedia(TortoiseModel):
    id = fields.UUIDField(pk=True)
    problem = fields.ForeignKeyField("models.Problem", "medias")
    media_path = fields.CharField(max_length=255)


class Solution(TortoiseModel):
    id = fields.UUIDField(pk=True)
    text = fields.TextField()
    problem = fields.ForeignKeyField("models.Problem", related_name="solutions")
    author = fields.ForeignKeyField("models.User", related_name="solutions")
    time_created = fields.DatetimeField(auto_now=True)

    @classmethod
    async def all(cls, using_db=None):
        return await (
            super()
            .all(using_db)
            .prefetch_related("medias")
            .select_related("author")
        )

    @classmethod
    async def get_or_none(cls, *args, using_db=None, **kwargs):
        return await (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .prefetch_related("medias")
            .select_related("author")
        )


class SolutionMedia(TortoiseModel):
    id = fields.UUIDField(pk=True)
    solution = fields.ForeignKeyField("models.Solution", "medias")
    media_path = fields.CharField(max_length=255)
