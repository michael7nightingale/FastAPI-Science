import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import FastAPI, APIRouter
from shutil import rmtree
import os.path
from tortoise import Tortoise

from app.app.routes.api import (
    main_router,
    auth_router,
    science_router,
    cabinets_router,
    problems_router,

)
from app.core.server import Server
from app.db.models import User


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.new_event_loop()


@pytest_asyncio.fixture(scope='session')
async def app() -> FastAPI:
    server = Server(test=True, use_cookies=False)
    await Tortoise.init(
        {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": "example.sqlite3"},
                }
            },
            "apps": {
                "models": {"models": ["app.db.models"], "default_connection": "default"}
            },
        },
        _create_db=True
    )
    await Tortoise.generate_schemas()
    await clear_users()
    await server._load_data()
    yield server.app
    await clear_users()
    await Tortoise._drop_databases()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8000/api/v1/") as client_:
        yield client_


@pytest_asyncio.fixture
def user1():
    return {
        "username": "michael7",
        "password": "password",
        "email": "asd2asd@gmail.com"
    }


@pytest_asyncio.fixture
def user2():
    return {
        "username": "michaasdael7",
        "password": "password123",
        "email": "asdaghhksd@gmail.com"
    }


async def clear_users():
    users = await User.all()
    for user in users:
        await user.delete()


@pytest_asyncio.fixture
async def client_user1(client: AsyncClient, users_test_data: dict, user1: dict):
    user_token_data = {
        "username": user1['username'],
        "password": user1['password']
    }
    response = await client.post(
        get_auth_url("get_token"),
        json=user_token_data
    )
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    client.headers = headers
    yield client
    await clear_users()


@pytest_asyncio.fixture
async def client_user2(client: AsyncClient, users_test_data: dict, user2: dict):
    user_token_data = {
        "username": user2['username'],
        "password": user2['password']
    }
    response = await client.post(
        get_auth_url("get_token"),
        json=user_token_data
    )
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    client.headers = headers
    client.cookies = headers
    yield client
    await clear_users()


@pytest_asyncio.fixture
async def users_test_data(app: FastAPI, user1: dict, user2: dict):
    await clear_users()
    user1_ = await User.register(**user1)
    await User.activate(user1_.id)
    user2_ = await User.register(**user2)
    await User.activate(user2_.id)
    users = user1_, user2_
    yield users
    users_paths = tuple((os.path.join(app.state.STATIC_DIR, str(user.id)) for user in users))
    for path in users_paths:
        if os.path.exists(path):
            rmtree(path)
    await clear_users()


@pytest_asyncio.fixture
def user_not_activated():
    return {
        "username": "Notactive",
        "password": "veryactivenot",
        "email": 'notactive229@gmail.com'
    }


@pytest_asyncio.fixture
async def not_active_user(app: FastAPI, user_not_activated: dict):
    await clear_users()
    user = await User.register(**user_not_activated)
    yield user
    await clear_users()


def url_for(router: APIRouter):
    def inner(name: str, **kwargs) -> str:
        return router.url_path_for(name, **kwargs)
    return inner


get_main_url = url_for(main_router)
get_auth_url = url_for(auth_router)
get_science_router = url_for(science_router)
get_cabinet_router = url_for(cabinets_router)
get_problem_router = url_for(problems_router)
