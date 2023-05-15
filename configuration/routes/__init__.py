from app.configuration.routes.routes import *
from app.internal import main, users, science


__routes__ = Routes(routes=(main.main_router, users.users_router, science.science_router))





