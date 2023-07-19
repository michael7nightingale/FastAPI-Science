from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import Type

from app.core.config import get_app_settings
from app.db.repositories.base import BaseRepository


def _get_pool(request: Request) -> async_sessionmaker:
    """Session maker pool is placed in fullstack`s state on fullstack`s startapp"""
    return request.app.state.pool


async def _get_session(pool=Depends(_get_pool)):
    """Save get and close the session"""
    async with pool() as session:
        yield session


def _get_socket_pool(func):
    settings = get_app_settings()
    engine = create_async_engine(settings.db_uri)
    pool = async_sessionmaker(bind=engine)

    def inner(pool_=pool, *args, **kwargs):
        return func(pool_=pool_, *args, **kwargs)

    return inner


@_get_socket_pool
async def _get_socket_session(pool_: async_sessionmaker):
    async with pool_() as session:
        yield session


def get_socket_repository(repo_type: Type[BaseRepository]):
    """Get repository instance after getting the session."""

    def _get_repo(session=_get_socket_session) -> BaseRepository:
        return repo_type(next(session()))

    return _get_repo


def get_repository(repo_type: Type[BaseRepository]):
    """Get repository instance after getting the session."""
    def _get_repo(session=Depends(_get_session)) -> BaseRepository:
        return repo_type(session)
    return _get_repo
