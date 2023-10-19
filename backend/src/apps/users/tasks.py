from asgiref.sync import async_to_sync

from .proxy import send_activation_email_task_proxy, clear_activation_codes_task_proxy
from src.core.celery import app


@app.task
def send_activation_email_task(email: str, name: str) -> None:
    return async_to_sync(send_activation_email_task_proxy)(email, name)


@app.task
def clear_activation_codes_task():
    return async_to_sync(clear_activation_codes_task_proxy)()
