from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse, RedirectResponse

from .dependencies import HistoryParser
from .models import History
from .schemas import HistoryListSchema
from .services import delete_history
from ..users.permissions import login_required

router = APIRouter(prefix="/cabinet", tags=["Cabinets"])


@router.get('/history', response_model=list[HistoryListSchema])
@login_required
async def history_list_view(request: Request):
    """History view."""
    history_list = await History.filter(user__id=request.user.id).select_related("formula", "formula__category")
    return [
        {
            **history.as_dict(),
            "formula": history.formula.as_dict(),
            "category": history.formula.category.as_dict(),
        }
        for history in history_list
    ]


@router.post('/history/download')
@login_required
async def history_download_view(request: Request, filedata: str = Depends(HistoryParser())):
    if filedata is not None:
        filepath, filename = filedata
        return FileResponse(path=filepath, filename=filename)
    else:
        return RedirectResponse(url=router.url_path_for('history'), status_code=303)


@router.delete('/history')
@login_required
async def history_delete_view(request: Request):
    await delete_history(request.user)
    return {"detail": "History deletes successfully"}
