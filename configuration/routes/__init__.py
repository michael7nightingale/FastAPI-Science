from configuration.routes.routes import *
from internal import main, users, science, api


__routes__ = Routes(
    routes=(
        main.main_router,
        users.users_router,
        science.science_router,
        api.api_router
    )
)





