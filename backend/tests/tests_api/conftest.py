import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import FastAPI, APIRouter
from shutil import rmtree
import os.path
from tortoise import Tortoise

from src.apps.users.routes import auth_router
from src.apps.sciences.routes import science_router
from src.apps.main.routes import main_router
from src.apps.cabinets.routes import cabinets_router
from src.apps.problems.routes import problems_router
from src.core.app import Server
from src.apps.users.models import User


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.new_event_loop()


@pytest_asyncio.fixture(scope='session')
async def app() -> FastAPI:
    server = Server()
    await Tortoise.init(
        {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": "example.sqlite3"},
                }
            },
            "apps": {
                "models": {"models": [
                    'src.apps.users.models',
                    'src.apps.main.models',
                    'src.apps.sciences.models',
                    'src.apps.problems.models',
                    'src.apps.cabinets.models',
                ], "default_connection": "default"}
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


def url_for(router: APIRouter):
    def inner(name: str, **kwargs) -> str:
        return router.url_path_for(name, **kwargs)
    return inner


@pytest_asyncio.fixture
def user1_data():
    return {
        "username": "michael7",
        "password": "password",
        "email": "asd2asd@gmail.com"
    }


@pytest_asyncio.fixture
def user2_data():
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
async def client_user1(client: AsyncClient, users_test_data: dict, user1_data: dict):
    user_token_data = {
        "login": user1_data['username'],
        "password": user1_data['password']
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
async def client_user2(client: AsyncClient, users_test_data: dict, user2_data: dict):
    user_token_data = {
        "login": user2_data['username'],
        "password": user2_data['password']
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
async def users_test_data(app: FastAPI, user1_data: dict, user2_data: dict):
    await clear_users()
    user1_ = await User.register(**user1_data)
    await user1_.activate()
    user2_ = await User.register(**user2_data)
    await user2_.activate()
    users = user1_, user2_
    yield users
    users_paths = tuple((os.path.join(app.state.STATIC_DIR, str(user.id)) for user in users))
    for path in users_paths:
        if os.path.exists(path):
            rmtree(path)
    await clear_users()


@pytest_asyncio.fixture
async def user1(users_test_data: tuple):
    return users_test_data[0]


@pytest_asyncio.fixture
async def user2(users_test_data: tuple):
    return users_test_data[1]


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


get_main_url = url_for(main_router)
get_auth_url = url_for(auth_router)
get_science_url = url_for(science_router)
get_cabinet_url = url_for(cabinets_router)
get_problem_url = url_for(problems_router)
