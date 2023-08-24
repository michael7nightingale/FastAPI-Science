from tortoise import fields

from src.base.models import TortoiseModel


class Problem(TortoiseModel):
    title = fields.CharField(max_length=255)
    text = fields.TextField()
    user = fields.ForeignKeyField("models.User", related_name="problems")
    # solution = fields.OneToOneField("models.Solution", related_name="problem_solved", null=True)
    science = fields.ForeignKeyField("models.Science", related_name="science")
    is_solved = fields.BooleanField(default=False)
    time_opened = fields.DatetimeField(auto_now=True)
    time_solved = fields.DatetimeField(null=True)

    @classmethod
    def all(cls, using_db=None):
        return (
            super()
            .all(using_db)
            .prefetch_related("medias")
            .select_related("science", "user")
        )

    @classmethod
    def get_or_none(cls, *args, using_db=None, **kwargs):
        return (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .prefetch_related("medias", "solutions")
            .select_related("science", "user")
        )


class ProblemMedia(TortoiseModel):
    problem = fields.ForeignKeyField("models.Problem", "medias")
    media_path = fields.CharField(max_length=255)


class Solution(TortoiseModel):
    text = fields.TextField()
    problem = fields.ForeignKeyField("models.Problem", related_name="solutions")
    author = fields.ForeignKeyField("models.User", related_name="solutions")
    time_created = fields.DatetimeField(auto_now=True)

    @classmethod
    def all(cls, using_db=None):
        return (
            super()
            .all(using_db)
            .prefetch_related("medias")
            .select_related("author")
        )

    @classmethod
    def get_or_none(cls, *args, using_db=None, **kwargs):
        return (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .prefetch_related("medias")
            .select_related("author")
        )


class SolutionMedia(TortoiseModel):
    solution = fields.ForeignKeyField("models.Solution", "medias")
    media_path = fields.CharField(max_length=255)
