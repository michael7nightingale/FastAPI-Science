from fastapi import APIRouter, Request, Body, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi_authtools import login_required
import os

from app.app.dependencies import get_repository, get_table_filepath
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
    history_list = await history_repo.all()
    return history_list


@cabinets_router.post('/download-history')
@login_required
async def history_download(
        request: Request,
        filedata: str = Depends(get_table_filepath)
):
    if filedata is not None:
        filepath, filename = filedata
        return FileResponse(path=filepath, filename=filename)
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
