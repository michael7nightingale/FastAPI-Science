from app.app.routes.main import main_router
from app.app.routes.auth import auth_router
from app.app.routes.cabinets import cabinets_router
from app.app.routes.sciences import science_router
from app.app.routes.problems import problems_router


__routers__ = (
    main_router,
    cabinets_router,
    science_router,
    auth_router,
    problems_router,

)
