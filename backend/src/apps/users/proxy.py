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
    create_smtp_server().send_email_message(
        subject="Registration",
        to_addrs=[email],
        body=message
    )
    await create_redis_client().set(f"code{code}", json.dumps(cache_data))


async def clear_activation_codes_task_proxy() -> None:
    redis_client = await create_redis_client()
    keys = await redis_client.keys()
    delete_keys = set()
    for key in keys:
        if key[:4] != "code":
            continue
        cache_data = json.loads(await redis_client.get(key))
        if not isinstance(cache_data, dict):
            continue
        if "exp" not in cache_data:
            continue
        now_datetime = datetime.datetime.now()
        exp_datetime = datetime.datetime.strptime(cache_data["exp"], "%d/%m/%y %H:%M:%S.%f")
        if now_datetime >= exp_datetime:
            delete_keys.add(key)
    if len(delete_keys):
        await redis_client.delete(*delete_keys)
