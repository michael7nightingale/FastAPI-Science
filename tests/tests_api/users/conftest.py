import os
from shutil import rmtree
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.apps.users.api_routes import auth_router
from src.apps.users.models import User
from ..conftest import url_for

get_auth_url = url_for(auth_router)


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
        "username": user1_data['username'],
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
        "username": user2_data['username'],
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
    await User.activate(user1_.id)
    user2_ = await User.register(**user2_data)
    await User.activate(user2_.id)
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
