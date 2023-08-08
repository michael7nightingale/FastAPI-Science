from uuid import uuid4

from tortoise import fields

from src.base.models import TortoiseModel


class History(TortoiseModel):
    formula = fields.ForeignKeyField("models.Formula")
    result = fields.FloatField()
    date_time = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField("models.User")

    @classmethod
    def all(cls, using_db=None):
        return (
            super()
            .all(using_db)
            .select_related("formula")
        )

    @classmethod
    def filter(cls, *args, **kwargs):
        return (
            super()
            .filter(*args, **kwargs)
            .select_related("formula", "user")
        )

    @classmethod
    def get_or_none(cls, *args, using_db=None, **kwargs):
        return (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .select_related("formula")
        )
