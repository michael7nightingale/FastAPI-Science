from .base import BaseAppSettings


class TestAppSettings(BaseAppSettings):
    DB_DRIVER: str
    DB_NAME: str
    DEBUG: bool = True

    @property
    def db_uri(self) -> str:
        return f"{self.DB_DRIVER}:///{self.DB_NAME}"

    class Config:
        env_file = ".test.env"
