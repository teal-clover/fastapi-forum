from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import forum.user.dependencies as dependencies
from forum.base.database import get_session
from forum.base.repository import RepositoryBase
from forum.user import schemas
from forum.user.models import User


class UserDBRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return users

    async def read_one(self, id: int) -> User | None:
        stmt = select(User).filter(User.id == id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def create(self, user: schemas.UserCreate) -> User:
        fake_hashed_password = dependencies.get_password_hash(user.password)
        db_user = User(email=user.email, hashed_password=fake_hashed_password)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def update(self, user_id: int, user: schemas.UserUpdate) -> User:
        db_user = await self.read_one(user_id)
        db_user.email = user.email
        await self.session.commit()

        await self.session.refresh(db_user)

        return db_user

    async def delete(self, user_id: int) -> User:
        db_user = await self.read_one(user_id)
        await self.session.delete(db_user)
        await self.session.commit()
        return db_user

    async def read_one_by_email(self, email: str) -> User | None:
        stmt = select(User).filter(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user


def get_user_repository():
    def func(session: AsyncSession = Depends(get_session)):
        return UserDBRepository(session)

    return func


UserRepository = Annotated[UserDBRepository, Depends(get_user_repository())]
