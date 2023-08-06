from src.base.apps import BaseConfig
from .routes import auth_router
from .api_routes import auth_router as api_auth_router


class UsersConfig(BaseConfig):
    static_directory = "src/apps/users/public/"
    static_path = "/static"
    static_name = "static_users"
    router = auth_router
    api_router = api_auth_router
