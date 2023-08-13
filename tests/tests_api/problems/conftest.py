import os
from shutil import rmtree

import pytest_asyncio
from fastapi import FastAPI

from src.apps.problems.models import Problem
from ..sciences.conftest import physics, mathem


@pytest_asyncio.fixture
async def problems_test_data(app: FastAPI, users_test_data, physics):
    user1, user2 = users_test_data
    problem1_user1 = await Problem.create(
        user_id=user1.id,
        title="How to run Maria DB in the Docker.",
        text="SOS Help me please",
        science_id=physics.id
    )

    problems = problem1_user1,
    problems_paths = tuple((os.path.join(app.state.STATIC_DIR, f"problems/problems/{problem.id}") for problem in problems))
    for path in problems_paths:
        os.makedirs(path)
    yield problems
    problems_paths = tuple(
        (os.path.join(app.state.STATIC_DIR, f"problems/problems/{problem.id}") for problem in (await Problem.all())))
    for path in problems_paths:
        if os.path.exists(path):
            rmtree(path)


@pytest_asyncio.fixture
async def problem1_user1(problems_test_data: tuple):
    return problems_test_data[0]


@pytest_asyncio.fixture
async def problem_create1_data(mathem) -> dict:
    return {
        "title": "Equations madness",
        "text": "This is incredible!",
        "science_id": mathem.id
    }
