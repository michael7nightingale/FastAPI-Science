from src.base.apps import BaseConfig
from .routes import cabinets_router
from .api_routes import cabinets_router as api_cabinets_router


class CabinetsConfig(BaseConfig):
    static_directory = "src/apps/cabinets/public/static/"
    static_path = "/static"
    static_name = "static_cabinets"
    router = cabinets_router
    api_router = api_cabinets_router
