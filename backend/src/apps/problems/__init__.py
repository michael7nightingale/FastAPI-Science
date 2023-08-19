from src.base.apps import BaseConfig
from .routes import problems_router
from .api_routes import problems_router as api_problems_router


class ProblemsConfig(BaseConfig):
    router = problems_router
    api_router = api_problems_router
