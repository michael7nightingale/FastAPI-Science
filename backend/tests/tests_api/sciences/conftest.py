import pytest_asyncio

from backend.src.apps.sciences.models import Science


@pytest_asyncio.fixture
async def physics():
    return await Science.get(slug="physics")


@pytest_asyncio.fixture
async def mathem():
    return await Science.get(slug="mathem")
