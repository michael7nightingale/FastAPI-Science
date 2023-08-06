from src.base.apps import BaseConfig
from .routes import science_router
from .api_routes import science_router as api_science_router


class SciencesConfig(BaseConfig):
    static_directory = "src/apps/sciences/public/"
    static_path = "/static/sciences"
    static_name = "static_sciences"
    router = science_router
    api_router = api_science_router
