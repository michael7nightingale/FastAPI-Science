from fastapi import Depends, Request

from app.db.repositories import ScienceRepository
from app.api.dependencies import get_repository


async def get_all_sciences(
        request: Request,
        science_repo: ScienceRepository = Depends(get_repository(ScienceRepository))
):
    sciences = await science_repo.all()
    return sciences
