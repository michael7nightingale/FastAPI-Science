from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi_authtools import AuthManager
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from starlette.responses import RedirectResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from app.core.config import get_app_settings, get_test_app_settings
from app.app.routes import __routers__, __api_routers__
from app.models.schemas import UserCustomModel
from app.db import register_db
from app.db.events import create_superuser
from app.data.load_data import load_all_data
from app.services.email import create_server, EmailService


class Server:
    def __init__(self, test: bool = False, use_cookies: bool = True):
        self.test = test
        self.use_cookies = use_cookies
        self._app = FastAPI()
        if test:
            self._settings = get_test_app_settings()
        else:
            self._settings = get_app_settings()
        self._engine: AsyncEngine
        self._pool: async_sessionmaker

        self._configurate_db()
        self._configurate_app()
        self._configure_services()

    @property
    def app(self) -> FastAPI:
        return self._app

    @property
    def settings(self):
        return self._settings

    def _configurate_app(self) -> None:
        """Configurate FastAPI application."""
        # including routers
        for router in __routers__:
            self.app.include_router(router)
        for api_router in __api_routers__:
            self.app.include_router(api_router, prefix="/api/v1")
        # event handlers settings
        self.app.add_event_handler(event_type="startup", func=self._on_startup_event)
        self.app.add_event_handler(event_type="shutdown", func=self._on_shutdown_event)
        # error handlers settings
        ErrorHandler.configure_app_error_handlers(self.app)
        # auth manager settings
        self.app.state.auth_manager = AuthManager(
            app=self.app,
            use_cookies=self.use_cookies,
            user_model=UserCustomModel,
            algorithm=self.settings.ALGORITHM,
            secret_key=self.settings.SECRET_KEY,
            expire_minutes=self.settings.EXPIRE_MINUTES,
        )
        # static files settings
        self.app.mount("/static", StaticFiles(directory="app/public/static/"), name='static')
        self.app.state.STATIC_DIR = "app/public/static/"

    def _configurate_db(self) -> None:
        """Configurate database."""
        register_db(
            app=self.app,
            modules=['app.db.models'],
            db_uri=self.settings.db_uri
        )

    def _configure_services(self):
        """SMTP server configuration for sending email messages."""
        self._smpt_server = create_server()
        self.app.state.email_service = EmailService(smtp_server=self._smpt_server)

    async def _load_data(self):
        """Data loading function."""
        await create_superuser(settings=self.settings)
        await load_all_data()

    async def _on_startup_event(self):
        """Startup handler."""
        await self._load_data()

    async def _on_shutdown_event(self):
        """Shutdown handler."""
        self._smpt_server.close()


class ErrorHandler:
    """Error handler class."""
    templates = Jinja2Templates(directory="app/public/templates/error")

    @classmethod
    def configure_app_error_handlers(cls, app: FastAPI):
        app.add_exception_handler(
            exc_class_or_status_code=HTTPException,
            handler=cls.http_exception_handler
        )

    @classmethod
    async def http_exception_handler(cls, request: Request, exc):
        if "api" in request.url.path:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
        else:
            if exc.status_code == 401:
                return RedirectResponse(request.app.url_path_for("login_get"), status_code=303)
            return cls.templates.TemplateResponse(f"{exc.status_code}.html", {"request": request})
