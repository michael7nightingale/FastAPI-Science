from fastapi import FastAPI

from app.core.server import Server


def create_app(*args, **kwargs) -> FastAPI:
    return Server().app
