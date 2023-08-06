from fastapi import Request

from .models import Science


async def get_all_sciences(request: Request):
    sciences = await Science.all()
    return sciences
