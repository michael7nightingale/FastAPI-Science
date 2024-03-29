from fastapi import FastAPI
from fastapi_authtools import AuthManager
from starlette.staticfiles import StaticFiles

from src.apps import __routers__
from src.core.config import get_app_settings
from src.apps.users.schemas import UserCustomModel
from src.core.middleware.time import process_time_middleware
from .middleware.cors import use_cors_middleware
from .middleware.authentication import use_authentication_middleware
from src.db.events import create_superuser, register_mongodb_db, register_db, authentication_user_getter
from src.db.redis import create_redis_client
from src.data.load_data import load_all_data, load_all_data_mongo


class Application:

    def __init__(self):
        self._settings = get_app_settings()
        self._app = FastAPI(debug=self.settings.DEBUG)

        self._configurate_db()
        self._configurate_app()
        self._configure_services()
        self._configurate_middleware()

    @property
    def app(self) -> FastAPI:
        return self._app

    @property
    def settings(self):
        return self._settings

    def _configurate_app(self) -> None:
        """Configurate FastAPI application."""
        # including routers
        # event handlers settings
        for router in __routers__:
            self.app.include_router(router, prefix="/api/v1")
        self.app.add_event_handler(event_type="startup", func=self._on_startup_event)
        self.app.add_event_handler(event_type="shutdown", func=self._on_shutdown_event)
        self.app.state.SECRET_KEY = self.settings.SECRET_KEY

        # auth manager settings
        self.app.state.auth_manager = AuthManager(
            app=self.app,
            use_cookies=False,
            user_model=UserCustomModel,
            algorithm=self.settings.ALGORITHM,
            secret_key=self.settings.SECRET_KEY,
            expire_minutes=self.settings.EXPIRE_MINUTES,
            user_getter=authentication_user_getter,
        )
        self.app.mount("/static", StaticFiles(directory="src/public/static/"), name="static")
        self.app.state.STATIC_DIR = "src/public/static/"

    def _configurate_middleware(self) -> None:
        use_cors_middleware(self.app)
        use_authentication_middleware(self.app)
        self.app.middleware("http")(process_time_middleware)

    def _configurate_db(self) -> None:
        """Configurate database."""
        self.app.state.mongodb_db = register_mongodb_db(self.settings.MONGODB_URL, self.settings.MONGODB_NAME)
        self.app.state.redis = create_redis_client(self.settings.REDIS_URL)
        register_db(
            app=self.app,
            modules=[
                'src.apps.users.models',
                'src.apps.sciences.models',
                'src.apps.cabinets.models',
            ],
            db_uri=self.settings.db_uri,
        )

    def _configure_services(self):
        """SMTP server configuration for sending email messages."""
        # self._smpt_server = create_smtp_server(
        #     host=self.settings.EMAIL_HOST,
        #     port=self.settings.EMAIL_PORT,
        #     password=self.settings.EMAIL_PASSWORD,
        #     user=self.settings.EMAIL_USER
        # )

    async def _load_data(self):
        """Data loading function."""
        await create_superuser(settings=self.settings)
        await load_all_data()
        await load_all_data_mongo(self.app.state.mongodb_db)

    async def _on_startup_event(self):
        """Startup handler."""
        await self._load_data()

    async def _on_shutdown_event(self):
        """Shutdown handler."""
        # self._smpt_server.close()
