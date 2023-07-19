from .main import main_router
from .sciences import science_router
from .auth import auth_router
from .problems import problems_router
from .cabinets import cabinets_router


__api_routers__ = (
    main_router,
    science_router,
    auth_router,
    problems_router,
    cabinets_router,

)
