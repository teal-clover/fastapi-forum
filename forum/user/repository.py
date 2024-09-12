from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from forum.database import DBSession, get_session
from forum.user import schemas
from forum.user.models import User


class UserDBRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_all(self, skip: int = 0, limit: int = 100):
        stmt = select(User).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return users

    async def read_one(self, id: int):
        stmt = select(User).filter(User.id == id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create(self, user: schemas.UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(
            email=user.email, hashed_password=fake_hashed_password)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def update(self, user_id: int, user: schemas.UserUpdate):
        db_user = await self.read_one(user_id)
        print(db_user)
        db_user.email = user.email
        print(db_user)
        await self.session.commit()

        await self.session.refresh(db_user)

        return db_user

    async def delete(self, user_id: int):
        db_user = await self.read_one(user_id)
        await self.session.delete(db_user)
        await self.session.commit()
        return db_user

    async def read_one_by_email(self, email: str):
        stmt = select(User).filter(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user


def get_user_repository():
    def func(session: AsyncSession = Depends(get_session)):
        return UserDBRepository(session)

    return func


UserRepository = Annotated[UserDBRepository, Depends(get_user_repository())]
