from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from app.services.hash import hash_password


async def create_superuser(session: AsyncSession, settings):
    try:
        user = User(
            username=settings.superuser_username,
            password=hash_password(settings.superuser_password),
            email=settings.superuser_email
        )
        session.add(user)
        await session.commit()
    except IntegrityError:
        pass
