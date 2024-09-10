from fastapi import HTTPException
from sqlalchemy import select

from forum import models
from forum.database import AsyncSession

from . import schemas


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
