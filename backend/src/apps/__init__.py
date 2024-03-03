from .main.routes import router as main_router
from .cabinets.routes import router as cabinets_router
from .users.routes import router as users_router
from .sciences.routes import router as sciences_router


__routers__ = (
    users_router,
    main_router,
    cabinets_router,
    sciences_router,

)
