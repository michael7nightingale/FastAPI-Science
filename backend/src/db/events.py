from tortoise.exceptions import IntegrityError
from motor.motor_asyncio import AsyncIOMotorClient

from src.apps.users.models import User
from src.services.hash import hash_password


async def create_superuser(settings) -> None:
    try:
        await User.create(
            username=settings.SUPERUSER_USERNAME,
            password=hash_password(settings.SUPERUSER_PASSWORD),
            email=settings.SUPERUSER_EMAIL
        )
    except IntegrityError:
        pass


def create_mongodb_db(db_url: str, db_name: str):
    client = AsyncIOMotorClient(db_url)
    return getattr(client, db_name)
