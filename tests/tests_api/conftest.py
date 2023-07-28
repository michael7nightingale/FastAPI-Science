import os.path
from shutil import rmtree

import pytest_asyncio
from httpx import AsyncClient
from fastapi import FastAPI, APIRouter

from app.app.routes.api import (
    main_router,
    auth_router,
    science_router,
    cabinets_router,
    problems_router,

)
from app.core.server import Server
from app.db import Base
from app.db.services import UserService


@pytest_asyncio.fixture
async def app() -> FastAPI:
    server = Server(test=True, use_cookies=False)
    async with server.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await server._load_data()
    yield server.app
    async with server.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8000/api/v1/") as client_:
        yield client_


@pytest_asyncio.fixture
def user1():
    return {
        "username": "michael7",
        "password": "password",
        "email": "asdasd@gmail.com"
    }


@pytest_asyncio.fixture
def user2():
    return {
        "username": "michaasdael7",
        "password": "password123",
        "email": "asdaghhksd@gmail.com"
    }


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


@pytest_asyncio.fixture
async def users_test_data(app: FastAPI, user1: dict, user2: dict):
    async with app.state.pool() as session:
        users_repo = UserService(session)
        user1_ = await users_repo.register(user1)
        await users_repo.activate(user1_.id, user1_.email)
        user2_ = await users_repo.register(user2)
        await users_repo.activate(user2_.id, user2_.email)
        users = user1_, user2_
        yield users
        users_paths = tuple((os.path.join(app.state.STATIC_DIR, user.id) for user in users))
        for path in users_paths:
            if os.path.exists(path):
                rmtree(path)


@pytest_asyncio.fixture
def user_not_activated():
    return {
        "username": "Notactive",
        "password": "veryactivenot",
        "email": 'notactive229@gmail.com'
    }


@pytest_asyncio.fixture
async def not_active_user(app: FastAPI, user_not_activated: dict):
    async with app.state.pool() as session:
        user_repo = UserService(session)
        user = await user_repo.register(user_not_activated)
        yield user


def url_for(router: APIRouter):
    def inner(name: str, **kwargs) -> str:
        return router.url_path_for(name, **kwargs)
    return inner


get_main_url = url_for(main_router)
get_auth_url = url_for(auth_router)
get_science_router = url_for(science_router)
get_cabinet_router = url_for(cabinets_router)
get_problem_router = url_for(problems_router)
