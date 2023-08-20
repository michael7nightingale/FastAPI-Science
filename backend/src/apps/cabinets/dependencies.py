from fastapi import Request, Body
import os

from .models import History
from src.services.tables import CsvTableManager, PandasTableManager
from .schemas import DownloadFile

HISTORY_DIR = '/files/history/'


def get_field(record, value):
    field = record
    for attribute in value.split("."):
        field = getattr(field, attribute)
    return field


class HistoryParser:
    columns_match = {
        "result": "result",
        "formula_title": "formula.title",
        "formula": "formula.formula",
        "date_time": "date_time"
    }

    def parse_record(self, record):
        return {name: get_field(record, value) for name, value in self.columns_match.items()}

    async def __call__(
            self,
            request: Request,
            filedata: DownloadFile = Body(),
    ):
        history_list = await History.filter(user_id=request.user.id)
        filepath = request.app.state.STATIC_DIR + HISTORY_DIR + request.user.id + '.' + filedata.extension
        if filedata.extension == 'csv':
            table = CsvTableManager(filepath)
        else:
            table = PandasTableManager(filepath)
        if not history_list:
            yield None
        else:
            table.init_data(self.columns_match.keys())
            for record in history_list:
                table.add_line_dict(self.parse_record(record))
            table.save_data()
            filename = f"{filedata.filename}.{filedata.extension}"
            yield filepath, filename
            os.remove(filepath)
