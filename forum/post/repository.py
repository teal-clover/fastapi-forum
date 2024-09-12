from typing import Annotated
from fastapi import Depends
from sqlalchemy import select

from forum.database import AsyncSession, get_session
from forum.post import schemas
from forum.post.models import Post


class PostDBRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_all(self, skip: int = 0, limit: int = 100):
        stmt = select(Post).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return users

    async def create(self, post: schemas.PostCreate, user_id: int):
        db_post = Post(**post.model_dump(), owner_id=user_id)
        self.session.add(db_post)
        await self.session.commit()
        await self.session.refresh(db_post)
        return db_post


def get_post_repository():
    def func(session: AsyncSession = Depends(get_session)):
        return PostDBRepository(session)

    return func


PostRepository = Annotated[PostDBRepository, Depends(get_post_repository())]
