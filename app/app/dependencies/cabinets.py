from fastapi import Request, Form
import os

from app.db.models import History
from app.services.tables import CsvTableManager, PandasTableManager


HISTORY_DIR = '/files/history/'


async def get_table_filepath(
        request: Request,
        filename: str = Form(),
        extension: str = Form(),
):
    history_list = (i.as_dict() for i in await History.filter(user_id=request.user.id))
    if history_list:
        filepath = request.app.state.STATIC_DIR + HISTORY_DIR + request.user.id + '.' + extension

        if extension == 'csv':
            table = CsvTableManager(filepath)
        else:
            table = PandasTableManager(filepath)

        history_list_first = next(history_list)
        table.init_data(history_list_first.keys())
        table.add_line(history_list_first.values())
        for line in history_list:
            table.add_line(line.values())
        table.save_data()
        filename = f"{filename}.{extension}"
        yield filepath, filename
        os.remove(filepath)
    else:
        yield None
