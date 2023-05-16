import os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi_login import LoginManager
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from configuration.routes import __routes__


class Server:
    """
    Класс сервера. Отвечает за наcтройку экземпляра класса FastAPI.
    По большей мере красивая инкапсуляция, нежели жизненная необходимость.
    """
    __app: FastAPI

    def __init__(self, app: FastAPI, login_manager: LoginManager):
        self.__app = app
        self.__error_templates = None
        self.TEMPLATES_DIR = None
        self.STATIC_DIR = None
        self.PLOTS_DIR = None
        self.__check_directories()
        self.__configurate_app()
        self.__login_manager = login_manager
        self.__register_login_manager()
        self.__register_routes(app)
        # self.__register_events(app)

    @property
    def app(self):
        return self.__app

    @app.setter
    def app(self, _):
        assert True

    def __configurate_app(self):
        self.app.mount(self.STATIC_DIR, StaticFiles(directory=self.STATIC_DIR.lstrip("/")), name="static")
        self.__error_templates = Jinja2Templates(directory=os.getcwd() + self.TEMPLATES_DIR + "/error/")

        @self.app.exception_handler(RequestValidationError)
        async def validation_exc_handler(request: Request, exc):
            # print(exc)
            self.__error_templates = Jinja2Templates(directory=os.getcwd() + self.TEMPLATES_DIR + "/error/")
            return self.__error_templates.TemplateResponse("500.html", context={'request': request})

        @self.app.exception_handler(StarletteHTTPException)
        async def http_exc_handler(request: Request, exc):
            # print(exc)
            self.__error_templates = Jinja2Templates(directory=os.getcwd() + self.TEMPLATES_DIR + "/error/")
            if exc.status_code == 402:
                return RedirectResponse(url='/accounts/login', status_code=303)
            elif exc.status_code == 404:
                return self.__error_templates.TemplateResponse('404.html', context={'request': request})
            elif exc.status_code == 403:
                return self.__error_templates.TemplateResponse('403.html', context={'request': request})
            elif exc.status_code == 500:
                return self.__error_templates.TemplateResponse("500.html", context={'request': request})

    def __check_directories(self) -> None:
        """Checking if all important directories are existing. Otherwise, the app won`t be started."""
        self.STATIC_DIR = "/app/public/static/"
        self.TEMPLATES_DIR = "/app/public/templates/"
        self.PLOTS_DIR = "/plots/"
        assert os.path.exists(os.getcwd() + self.STATIC_DIR), f"Static directory does not exists: {self.STATIC_DIR}"
        assert os.path.exists(os.getcwd() + self.TEMPLATES_DIR), f"Template directory does not exists: {self.TEMPLATES_DIR}"
        # for temp in self.TEMPLATES_DIRS:
        #     assert os.path.exists(TEMPLATES_DIR + temp), f"Template subdirectory does not exists: {temp}"
        FULL_PLOT_PATH = os.getcwd() + self.STATIC_DIR + self.PLOTS_DIR
        if not os.path.exists(FULL_PLOT_PATH):  # plots dir may be created empty
            os.mkdir(FULL_PLOT_PATH)

    @staticmethod
    def __register_events(app):
        ...

    @staticmethod
    def __register_routes(app):
        __routes__.register_rotes(app)

    def __register_login_manager(self):
        self.__login_manager.useRequest(self.app)
