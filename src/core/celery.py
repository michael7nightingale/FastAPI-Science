from celery import Celery
from .config import get_app_settings


celery_application = Celery(__name__)
celery_application.config_from_object(get_app_settings(), namespace='CELERY')

celery_application.autodiscover_tasks(
    packages=[
        "src.apps.main",
        "src.apps.users",
        "src.apps.sciences",
        "src.apps.cabinets",
        "src.apps.problems",
    ]
)
