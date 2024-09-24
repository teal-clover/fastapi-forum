from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    future=True,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    session = AsyncSessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        print(e)
        await session.rollback()
    finally:
        await session.close()


DBSession = Annotated[AsyncSession, Depends(get_session)]
