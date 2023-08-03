from tortoise.exceptions import IntegrityError

from .models import User
from app.services.hash import hash_password


async def create_superuser(settings) -> None:
    try:
        await User.create(
            username=settings.SUPERUSER_USERNAME,
            password=hash_password(settings.SUPERUSER_PASSWORD),
            email=settings.SUPERUSER_EMAIL
        )
    except IntegrityError:
        pass
