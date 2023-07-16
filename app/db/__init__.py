from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine


def create_engine(db_uri: str) -> AsyncEngine:
    return create_async_engine(db_uri)


def create_pool(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False
    )


Base = declarative_base()
