from aioredis import from_url, Redis

from src.core.config import get_app_settings


def create_redis_client(redis_url: str = get_app_settings().REDIS_URL) -> Redis:
    return from_url(redis_url)
