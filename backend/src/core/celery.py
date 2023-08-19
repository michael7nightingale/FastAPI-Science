from celery import Celery
from .config import get_app_settings


celery_application = Celery(__name__)
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
