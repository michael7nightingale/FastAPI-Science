from datetime import datetime, timedelta

from tortoise import fields
from tortoise.exceptions import IntegrityError

from src.base.models import TortoiseModel
from src.services.password import hash_password, verify_password, generate_activation_code


class User(TortoiseModel):
    username = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=100, unique=True)
    first_name = fields.CharField(max_length=100, null=True)
    last_name = fields.CharField(max_length=100, null=True)
    is_superuser = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=False)
    time_registered = fields.DatetimeField(auto_now=True)
    last_login = fields.DatetimeField(auto_now_add=True, null=True)

    @classmethod
    async def login(cls, password: str, username: str | None = None, email: str | None = None):
        if username:
            user = await cls.get_or_none(username=username)
        elif email:
            user = await cls.get_or_none(email=email)
        else:
            return None, None
        print(123123, user)
        if user is not None:
            return user, verify_password(password, user.password)
        return None, None

    @classmethod
    async def register(cls, **kwargs):
        kwargs.update(password=hash_password(kwargs['password']))
        try:
            user = await cls.create(**kwargs, active=True)
        except IntegrityError:
            raise
            return
        return user

    async def activate(self) -> None:
        self.is_active = True
        await self.save()

    def __str__(self):
        return self.username

    def full_name(self) -> str:
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}"
        return self.username


class ActivationCode(TortoiseModel):
    user = fields.ForeignKeyField("models.User", related_name="activation_code")
    code = fields.CharField(max_length=6, default=generate_activation_code)
    expire = fields.DatetimeField()

    class Meta:
        ordering = ['-expire']

    @classmethod
    async def create_activation_code(cls, user: User):
        code = generate_activation_code()
        while (await cls.get_or_none(code=code)) is not None:
            code = generate_activation_code()
        return await cls.create(user=user, code=code, expire=datetime.now() + timedelta(hours=1))
