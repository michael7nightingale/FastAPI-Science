from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import Type

from app.db.repositories.base import BaseRepository


def _get_pool(request: Request) -> async_sessionmaker:
    """Session maker pool is placed in fullstack`s state on fullstack`s startapp"""
    return request.app.state.pool


async def _get_session(pool=Depends(_get_pool)):
    """Save get and close the session"""
    async with pool() as session:
        yield session


def get_repository(repo_type: Type[BaseRepository]):
    """Get repository instance after getting the session."""
    def _get_repo(session=Depends(_get_session)) -> BaseRepository:
        return repo_type(session)
    return _get_repo
