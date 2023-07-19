from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi_authtools import login_required

from app.app.dependencies import get_history_repository, get_table_filepath
from app.db.repositories import HistoryRepository


cabinets_router = APIRouter(prefix="/cabinet")


@cabinets_router.get('/history')
@login_required
async def history(history_repo: HistoryRepository = Depends(get_history_repository)):
    """History view."""
    history_list = await history_repo.all()
    return history_list


@cabinets_router.post('/download-history')
@login_required
async def history_download(filedata: str = Depends(get_table_filepath)):
    if filedata is not None:
        filepath, filename = filedata
        return FileResponse(path=filepath, filename=filename)
    else:
        return RedirectResponse(url=cabinets_router.url_path_for('history'), status_code=303)


@cabinets_router.post('/delete_history')
@login_required
async def history_delete(request: Request):
    return RedirectResponse(url=cabinets_router.url_path_for('history'), status_code=303)