from .base import BaseAppSettings


class ProdAppSettings(BaseAppSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    DEBUG: bool = False

    @property
    def db_uri(self) -> str:
        host_address = self.DB_HOST
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{host_address}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = "prod.env"
