from fastapi import Request, Form, Depends
import os

from app.app.dependencies.services import get_history_service
from app.db.services import HistoryService
from app.services.tables import CsvTableManager, PandasTableManager


HISTORY_DIR = '/files/history/'


async def get_table_filepath(
        request: Request,
        filename: str = Form(),
        extension: str = Form(),
        history_service: HistoryService = Depends(get_history_service)
):
    history_list = [
        i.as_dict() for i in await history_service.filter(user_id=request.user.id)
    ]
    if history_list:
        filepath = request.app.state.STATIC_DIR + HISTORY_DIR + request.user.id + '.' + extension

        if extension == 'csv':
            table = CsvTableManager(filepath)
        else:
            table = PandasTableManager(filepath)
        table.init_data(history_list[0].keys())
        for line in history_list:
            table.add_line(line.values())
        table.save_data()
        filename = f"{filename}.{extension}"
        yield filepath, filename
        os.remove(filepath)
    else:
        yield None
