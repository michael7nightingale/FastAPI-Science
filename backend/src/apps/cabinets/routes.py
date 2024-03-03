from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi_authtools import login_required

from .dependencies import HistoryParser
from .models import History
from .services import delete_history

router = APIRouter(prefix="/cabinet", tags=["Cabinets"])


@router.get('/history')
@login_required
async def history(request: Request):
    """History view."""
    history_list = await History.filter(user__id=request.user.id)
    return history_list


@router.post('/history/download')
@login_required
async def history(request: Request, filedata: str = Depends(HistoryParser())):
    if filedata is not None:
        filepath, filename = filedata
        return FileResponse(path=filepath, filename=filename)
    else:
        return RedirectResponse(url=router.url_path_for('history'), status_code=303)


@router.delete('/history')
@login_required
async def history(request: Request):
    await delete_history(request.user)
    return {"detail": "History deletes successfully"}
