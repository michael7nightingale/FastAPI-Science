from datetime import datetime

from fastapi import APIRouter


class BaseConfig:
    router: APIRouter
    api_router: APIRouter


def context_processor(request):
    return {
        "year": datetime.now().year,
        "author": "michael7nightingale"
    }
