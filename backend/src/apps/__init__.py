from .main.routes import main_router
from .users.routes import auth_router
from .problems.routes import problems_router
from .sciences.routes import science_router
from .cabinets.routes import cabinets_router


__routers__ = (
    main_router,
    auth_router,
    problems_router,
    science_router,
    cabinets_router,

)
