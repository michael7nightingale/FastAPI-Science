import datetime
import json

from src.db.redis import create_redis_client
from src.services.email import create_smtp_server
from src.services.token import generate_activation_code


async def send_activation_email_task_proxy(email: str, name: str) -> None:
    code = generate_activation_code(length=6)
    cache_data = {  # noqa: F841
        "email": email,
        "code": code,
        "exp": (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime("%d/%m/%y %H:%M:%S.%f")
    }
    message = "%s, вот ваш код для завершения регистрации: %s" % (name, code)
    create_smtp_server().send_message(
        subject="Registration",
        to_addrs=[email],
        body=message
    )
    await create_redis_client().set(code, json.dumps(cache_data))
