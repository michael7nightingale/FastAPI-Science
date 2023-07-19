from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi_authtools import AuthManager
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from app.core.config import get_app_settings
from app.app.routes import __routers__, __api_routers__
from app.models.schemas import UserCustomModel
from app.db import create_engine, create_pool


class Server:
    def __init__(self):
        self._app = FastAPI()
        self._settings = get_app_settings()
        self._engine: AsyncEngine
        self._pool: async_sessionmaker

        self._configurate_db()
        self._configurate_app()

    @property
    def app(self) -> FastAPI:
        return self._app

    @property
    def settings(self):
        return self._settings

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def pool(self) -> async_sessionmaker:
        return self._pool

    def _configurate_app(self) -> None:
        self.app.state.pool = self.pool
        for router in __routers__:
            self.app.include_router(router)

        for api_router in __api_routers__:
            self.app.include_router(api_router, prefix="/api/v1")

        self.app.add_event_handler(event_type="startup", func=self._on_startup_event)
        self.app.add_event_handler(event_type="shutdown", func=self._on_shutdown_event)
        ErrorTemplateHandler.configure_app_error_handlers(self.app)
        auth_manager = AuthManager(
            app=self.app,
            use_cookies=True,
            user_model=UserCustomModel,
            algorithm=self.settings.algorithm,
            secret_key=self.settings.secret_key,
            expire_minutes=self.settings.expire_minutes,
        )
        self.app.state.auth_manager = auth_manager
        self.app.mount("/static", StaticFiles(directory="app/public/static/"), name='static')

    def _configurate_db(self) -> None:
        self._engine = create_engine(self.settings.db_uri)
        self._pool = create_pool(self.engine)

    def _on_startup_event(self):
        pass

    def _on_shutdown_event(self):
        pass


class ErrorTemplateHandler:
    templates = Jinja2Templates(directory="app/public/templates/error")

    @classmethod
    def configure_app_error_handlers(cls, app: FastAPI):
        app.add_exception_handler(
            exc_class_or_status_code=HTTPException,
            handler=cls.http_exception_handler
        )

    @classmethod
    def http_exception_handler(cls, request: Request, exc):
        if "api" in request.url.path:
            return {"detail": exc}
        else:
            if exc.status_code == 401:
                return RedirectResponse(request.app.url_path_for("login_get"), status_code=303)
            return cls.templates.TemplateResponse(f"{exc.status_code}.html", {"request": request})
