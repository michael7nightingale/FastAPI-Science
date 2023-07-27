from fastapi import Depends, Request

from app.db.services import ScienceService
from app.app.dependencies.services import get_science_service


async def get_all_sciences(
        request: Request,
        science_service: ScienceService = Depends(get_science_service)
):
    sciences = await science_service.all()
    return sciences
