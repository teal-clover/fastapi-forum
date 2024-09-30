from typing import AsyncGenerator, AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from forum.base.database import get_session
from forum.base.models import Base
from forum.comment.models import Comment
from forum.main import app
from forum.post.models import Post
from forum.user.dependencies import get_password_hash
from forum.user.models import User


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def token(client: AsyncClient):
    response_token = await client.post(
        "/users/token", data={"username": "user2@email.com", "password": "password"}
    )

    token = response_token.json()["access_token"]
    return token


@pytest.fixture(scope="session")
def async_engine():
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"

    async_engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
    )
    return async_engine


@pytest.fixture(scope="session")
def local_session(async_engine):
    AsyncSessionLocal = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        future=True,
    )
    return AsyncSessionLocal


@pytest.fixture(scope="session")
async def populate_db(local_session: async_sessionmaker[AsyncSession]):
    session = local_session()
    async with session.begin():
        user1 = User(
            id=1,
            email="user1@email.com",
            hashed_password=get_password_hash("password"),
        )
        user2 = User(
            id=2,
            email="user2@email.com",
            hashed_password=get_password_hash("password"),
        )
        session.add_all([user1, user2])

    async with session.begin():
        post1 = Post(id=1, title="title1", content="content1", user_id=1)
        post2 = Post(id=2, title="title2", content="content2", user_id=1)
        session.add_all([post1, post2])

    async with session.begin():
        comment1 = Comment(id=1, content="content1", user_id=1, post_id=1)
        comment2 = Comment(id=2, content="content2", user_id=1, post_id=1)
        session.add_all([comment1, comment2])


@pytest.fixture(scope="session")
async def overrwrite_dependency(local_session: async_sessionmaker[AsyncSession]):
    async def test_get_session() -> AsyncIterator[async_sessionmaker]:
        session = local_session()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
        finally:
            await session.close()

    app.dependency_overrides[get_session] = test_get_session


@pytest.fixture(scope="session")
async def create_db(async_engine: AsyncEngine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def clear_db(async_engine: AsyncEngine):
    async def clear():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    return clear


@pytest.fixture(scope="session")
async def client(
    create_db, populate_db, overrwrite_dependency, clear_db
) -> AsyncGenerator:

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as client:
        yield client

    await clear_db()
