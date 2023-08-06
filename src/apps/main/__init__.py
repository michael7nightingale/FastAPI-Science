from src.base.apps import BaseConfig
from .routes import main_router
from .api_routes import main_router as api_main_router


class MainConfig(BaseConfig):
    router = main_router
    api_router = api_main_router
