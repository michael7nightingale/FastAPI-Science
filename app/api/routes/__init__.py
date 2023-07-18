from app.api.routes.main import main_router
from app.api.routes.auth import auth_router
from app.api.routes.cabinets import cabinets_router
from app.api.routes.sciences import science_router
from app.api.routes.problems import problems_router


__api_routers__ = (
    main_router,
    cabinets_router,
    science_router,
    auth_router,
    problems_router,

)
