from fastapi import FastAPI

from app.core.server import Server


def create_app() -> FastAPI:
    return Server().app
