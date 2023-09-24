from celery import Celery
import asyncio
from tortoise import run_async, Tortoise

from .config import get_app_settings


class AsyncCelery(Celery):

    def on_init(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        run_async(
            Tortoise.init(
                db_url=get_app_settings().db_uri,
                modules={
                    'models': [
                        'src.apps.users.models',
                        'src.apps.main.models',
                        'src.apps.sciences.models',
                        'src.apps.problems.models',
                        'src.apps.cabinets.models',
                    ]
                },
            )
        )


celery_application = AsyncCelery(__name__)
celery_application.config_from_object(get_app_settings(), namespace='CELERY')

celery_application.autodiscover_tasks(
    packages=[
        "backend.apps.main",
        "backend.apps.users",
        "backend.apps.sciences",
        "backend.apps.cabinets",
        "backend.apps.problems",
    ]
)
