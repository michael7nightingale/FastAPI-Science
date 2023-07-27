from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from app.services.hash import hash_password


async def create_superuser(session: AsyncSession, settings):
    try:
        user = User(
            username=settings.SUPERUSER_USERNAME,
            password=hash_password(settings.SUPERUSER_PASSWORD),
            email=settings.SUPERUSER_EMAIL
        )
        session.add(user)
        await session.commit()
    except IntegrityError:
        pass
