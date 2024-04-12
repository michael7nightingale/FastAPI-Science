from fastapi import APIRouter, Request


router = APIRouter(prefix='', tags=["Main"])


@router.get("/")
async def homepage(request: Request):
    """Main page."""
    return {"detail": "Application is started."}
