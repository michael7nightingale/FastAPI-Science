from app.api.routes.main import main_router
from app.api.routes.auth import auth_router
from app.api.routes.cabinets import cabinets_router
from app.api.routes.science import science_router

__routers__ = (main_router, cabinets_router, science_router, auth_router)
