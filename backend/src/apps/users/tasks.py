from asgiref.sync import async_to_sync

from .proxy import send_activation_email_task_proxy
from src.core.celery import app


@app.task
def send_activation_email_task(email: str, name: str) -> None:
    return async_to_sync(send_activation_email_task_proxy)(email, name)
