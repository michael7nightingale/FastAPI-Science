import sys

from celery import Celery
import asyncio
import nest_asyncio
from tortoise import run_async, Tortoise

from .config import get_app_settings


class AsyncCelery(Celery):

    def on_init(self):
        nest_asyncio.apply()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        run_async(
            Tortoise.init(
                db_url=get_app_settings().db_uri,
                modules={
                    'models': [
                        # 'src.apps.users.models',
                        # 'src.apps.sciences.models',
                        # 'src.apps.problems.models',
                        # 'src.apps.cabinets.models',
                    ]
                },
            )
        )


sys.path.append('./')

app = AsyncCelery(__name__)
app.config_from_object(get_app_settings(), namespace='CELERY')


app.autodiscover_tasks(
    packages=[
        "src.apps.users",
        "src.apps.sciences",
        "src.apps.cabinets",
        "src.apps.problems",
    ]
)
