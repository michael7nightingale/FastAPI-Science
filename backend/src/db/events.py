from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError
# from motor.motor_asyncio import AsyncIOMotorClient

from src.apps.users.models import User
from src.services.password import hash_password


def register_db(app: FastAPI, db_uri: str, modules: list) -> None:
    register_tortoise(
        app=app,
        generate_schemas=True,
        config={
            'connections': {
                'default': db_uri
            },
            'apps': {
                'models': {
                    'models': modules,
                    'default_connection': 'default',
                }
            },
        },
        add_exception_handlers=True,
    )


async def authentication_user_getter(*args, **kwargs):
    email = kwargs.get("email")
    user = await User.get_or_none(email=email)
    return user


async def create_superuser(settings) -> None:
    try:
        await User.create(
            username=settings.SUPERUSER_USERNAME,
            password=hash_password(settings.SUPERUSER_PASSWORD),
            email=settings.SUPERUSER_EMAIL
        )
    except IntegrityError:
        pass

# def register_mongodb_db(db_url: str, db_name: str):
#     client = AsyncIOMotorClient(db_url)
#     return getattr(client, db_name)
