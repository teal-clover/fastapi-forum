from fastapi import HTTPException
from sqlalchemy import select

from . import models, schemas
from .database import AsyncSession


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


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Post]:
    stmt = select(models.Post).offset(skip).limit(limit)
    result = await db.execute(stmt)
    posts = result.scalars().all()
    print(posts)
    return posts


async def create_user_post(db: AsyncSession, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.model_dump(), owner_id=user_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def update_user(db: AsyncSession, user_id: int, user: schemas.UserUpdate):
    db_user = await get_user(db, user_id)
    print(db_user)
    db_user.email = user.email
    print(db_user)
    await db.commit()

    # doesn't work without refresh, maybe related https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#asyncio-orm-avoid-lazyloads
    await db.refresh(db_user)

    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    await db.delete(db_user)
    await db.commit()
    return None
