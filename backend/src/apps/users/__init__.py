from src.base.apps import BaseConfig
from .routes import auth_router
from .api_routes import auth_router as api_auth_router


class UsersConfig(BaseConfig):
    router = auth_router
    api_router = api_auth_router
