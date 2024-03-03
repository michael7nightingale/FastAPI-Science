from fastapi import FastAPI

from src.core.app import Application


def create_app(*args, **kwargs) -> FastAPI:
    return Application().app


app = create_app()
