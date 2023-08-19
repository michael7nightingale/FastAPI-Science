from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


def register_db(app: FastAPI, db_uri: str, modules: list):
    register_tortoise(
        app=app,
        db_url=db_uri,
        modules={'models': modules},
        generate_schemas=True,
        add_exception_handlers=True
    )
