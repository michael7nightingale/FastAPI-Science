from fastapi import FastAPI
from app.configuration.server import Server
from app.internal.users import loginManager


def create_app(_=None) -> FastAPI:
    app = FastAPI()
    return Server(app, loginManager).app
