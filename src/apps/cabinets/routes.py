from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse
from fastapi_authtools import login_required

from .dependencies import HistoryParser
from .models import History


cabinets_router = APIRouter(prefix="/cabinets")
templates = Jinja2Templates('src/apps/cabinets/templates/')


@cabinets_router.get('/')
@login_required
async def cabinet(request: Request):
    """Personal cabinets main page view."""
    context = {"request": request}
    return templates.TemplateResponse("personal_cabinet.html", context=context)


@cabinets_router.get('/history')
@login_required
async def history(request: Request):
    """History view."""
    history_list = await History.filter(user_id=request.user.id)
    context = {
        "title": "История вычислений",
        "history": history_list,
        'request': request
    }
    return templates.TemplateResponse("history.html", context=context)


@cabinets_router.post('/download-history')
@login_required
async def history_download(
        request: Request,
        filedata: str = Depends(HistoryParser())
):
    if filedata is not None:
        filepath, filename = filedata
        return FileResponse(path=filepath, filename=filename)
    else:
        return RedirectResponse(url=cabinets_router.url_path_for('history'), status_code=303)


@cabinets_router.post('/delete_history')
@login_required
async def history_delete(request: Request):
    history_list = await History.filter(user__id=request.user.id)
    for h in history_list:
        await h.delete()
    return RedirectResponse(url=cabinets_router.url_path_for('history'), status_code=303)
