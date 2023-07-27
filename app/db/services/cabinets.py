from app.db.services.sqlalchemy_async import SQLAlchemyAsyncService
from app.db.models import History


class HistoryService(SQLAlchemyAsyncService):
    model = History
