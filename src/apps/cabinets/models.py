from tortoise import fields

from src.base.models import TortoiseModel


class History(TortoiseModel):
    id = fields.UUIDField(pk=True)
    formula = fields.ForeignKeyField("models.Formula")
    result = fields.FloatField()
    date_time = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField("models.User")

    @classmethod
    async def all(cls, using_db=None):
        return await (
            super()
            .all(using_db)
            .select_related("formula")
        )

    @classmethod
    async def get_or_none(cls, *args, using_db=None, **kwargs):
        return await (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .select_related("formula")
        )
