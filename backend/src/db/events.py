from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError
from motor.motor_asyncio import AsyncIOMotorClient

from src.apps.users.models import User
from src.services.hash import hash_password


def register_db(app: FastAPI, db_uri: str, modules: list) -> None:
    register_tortoise(
        app=app,
        db_url=db_uri,
        modules={'models': modules},
        generate_schemas=True,
        add_exception_handlers=True
    )


async def create_superuser(settings) -> None:
    try:
        await User.create(
            username=settings.SUPERUSER_USERNAME,
            password=hash_password(settings.SUPERUSER_PASSWORD),
            email=settings.SUPERUSER_EMAIL
        )
    except IntegrityError:
        pass


def register_mongodb_db(db_url: str, db_name: str):
    client = AsyncIOMotorClient(db_url)
    return getattr(client, db_name)
