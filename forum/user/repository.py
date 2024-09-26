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
        statement = select(User).offset(skip).limit(limit)
        response = await self.session.execute(statement)
        users = response.scalars().all()
        return users

    async def read_one(self, item_id: int) -> User | None:
        statement = select(User).filter(User.id == item_id)
        response = await self.session.execute(statement)
        user = response.scalar_one_or_none()
        return user

    async def create(self, item: schemas.UserCreate) -> User:
        fake_hashed_password = dependencies.get_password_hash(item.password)
        user = User(email=item.email, hashed_password=fake_hashed_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, item_id: int, item: schemas.UserUpdate) -> User:
        user = await self.read_one(item_id)
        user.email = item.email
        await self.session.commit()

        await self.session.refresh(user)

        return user

    async def delete(self, item_id: int) -> User:
        user = await self.read_one(item_id)
        await self.session.delete(user)
        await self.session.commit()
        return user

    async def read_one_by_email(self, email: str) -> User | None:
        statement = select(User).filter(User.email == email)
        response = await self.session.execute(statement)
        user = response.scalar_one_or_none()
        return user


def get_user_repository():
    def func(session: AsyncSession = Depends(get_session)):
        return UserDBRepository(session)

    return func


UserRepository = Annotated[UserDBRepository, Depends(get_user_repository())]
