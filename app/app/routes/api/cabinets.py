from fastapi import APIRouter, Request, Body, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi_authtools import login_required
import os

from app.app.dependencies import get_repository
from app.db.repositories import HistoryRepository


cabinets_router = APIRouter(prefix="/cabinet")
HISTORY_DIR = 'fullstack/public/static/data/'


@cabinets_router.get('/history')
@login_required
async def history(
        request: Request,
        history_repo: HistoryRepository = Depends(get_repository(HistoryRepository))
):
    """History view."""
    history_list = await history_repo.filter(user_id=request.user.id)
    return [i.as_dict() for i in history_list]


@cabinets_router.post('/download-history')
@login_required
async def history_download(request: Request, filename: str = Body()):
    history_list = []
    tables = []
    filepath = HISTORY_DIR + f'{request.user.id}.csv'
    table = tables.CsvTableManager(filepath)
    history_list = [i.as_dict() for i in history_list]

    if history_list:
        table.init_data(history_list[0].keys())
        for line in history_list:
            table.add_line(line.values())
        table.save_data(filepath)
        return FileResponse(path=filepath, filename=f"{filename}.csv")
    else:
        return RedirectResponse(url=cabinets_router.url_path_for('history'), status_code=303)


def delete_history_csv(user_id: int):
    """Delete .csv file with history."""
    path = HISTORY_DIR + f'{user_id}.csv'
    if os.path.exists(path):
        os.remove(path)
    else:
        return None


@cabinets_router.post('/delete_history')
@login_required
async def history_delete(request: Request):
    return RedirectResponse(url=cabinets_router.url_path_for('history'), status_code=303)
