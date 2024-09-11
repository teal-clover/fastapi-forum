from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_user(db: AsyncSession, user_id: int) -> models.User:
    stmt = select(models.User).filter(models.User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(models.User).filter(models.User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(models.User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    user = result.scalars().all()
    return user


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user: schemas.UserUpdate):
    db_user = await get_user(db, user_id)
    print(db_user)
    db_user.email = user.email
    print(db_user)
    await db.commit()

    await db.refresh(db_user)

    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    await db.delete(db_user)
    await db.commit()
    return None
