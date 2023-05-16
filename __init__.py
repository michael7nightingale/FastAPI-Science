from fastapi import FastAPI

from configuration.server import Server
from internal.users import loginManager


def create_app(_=None) -> FastAPI:
    app = FastAPI()
    return Server(app, loginManager).app
