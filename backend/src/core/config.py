import os
from functools import lru_cache

from .settings.base import BaseAppSettings, AppEnvTypes
from .settings.development import DevAppSettings
from .settings.production import ProdAppSettings
from .settings.test import TestAppSettings


environments = {
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
    AppEnvTypes.dev: DevAppSettings,

}


@lru_cache
def get_app_settings() -> BaseAppSettings:
    if os.getenv("DOCKER"):
        BaseAppSettings.Config.app_env = AppEnvTypes.prod
    env_type = BaseAppSettings.Config.app_env
    settings_cls = environments[env_type]
    return settings_cls()
