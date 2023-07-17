from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.base import BaseRepository
from app.db.models import History


class HistoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(History, session)
