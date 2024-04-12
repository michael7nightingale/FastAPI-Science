from tortoise import fields

from src.base.models import TortoiseModel


class Science(TortoiseModel):
    title = fields.CharField(max_length=40, unique=True, index=True)
    content = fields.TextField()
    image_path = fields.CharField(max_length=255, null=True)
    slug = fields.CharField(max_length=40, unique=True, index=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    @classmethod
    def get_or_none(cls, *args, using_db=None, **kwargs):
        return (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .prefetch_related("categories")
        )


class Category(TortoiseModel):
    title = fields.CharField(max_length=40, unique=True, index=True)
    content = fields.TextField()
    image_path = fields.CharField(max_length=255, null=True)
    science = fields.ForeignKeyField(
        model_name="models.Science",
        related_name="categories",
    )
    slug = fields.CharField(max_length=40, unique=True, index=True)
    is_special = fields.BooleanField(default=False)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    @classmethod
    def get_or_none(cls, *args, using_db=None, **kwargs):
        return (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .prefetch_related("formulas")
            .select_related("science")
        )


class Formula(TortoiseModel):
    title = fields.CharField(max_length=40, unique=True, index=True)
    content = fields.TextField()
    formula = fields.CharField(max_length=255)
    image_path = fields.CharField(max_length=255, null=True)
    category = fields.ForeignKeyField(
        model_name="models.Category",
        related_name="formulas"
    )
    slug = fields.CharField(max_length=40, unique=True, index=True)
    data = fields.JSONField(null=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_or_none(cls, *args, using_db=None, **kwargs):
        return (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .select_related("category", "category__science")
        )
