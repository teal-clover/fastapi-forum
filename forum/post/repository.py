from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select

from forum.base.database import AsyncSession, get_session
from forum.base.repository import RepositoryBase
from forum.post import schemas
from forum.post.models import Post


class PostDBRepository(RepositoryBase):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_all(self, skip: int = 0, limit: int = 100) -> Sequence[Post]:
        statement = select(Post).offset(skip).limit(limit)
        response = await self.session.execute(statement)
        users = response.scalars().all()
        return users

    async def create(self, item: schemas.PostCreate, user_id: int) -> Post:
        post = Post(**item.model_dump(), user_id=user_id)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def read_one(self, item_id: int) -> Post:
        statement = select(Post).filter(Post.id == item_id)
        response = await self.session.execute(statement)
        post = response.scalar_one_or_none()
        return post

    async def update(self, item_id, item: schemas.PostUpdate) -> Post:
        post = await self.read_one(item_id)
        post.title = item.title
        post.content = item.content

        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def delete(self, item_id: int) -> Post:
        post = await self.read_one(item_id)
        await self.session.delete(post)
        await self.session.commit()
        return post


def get_post_repository():
    def func(session: AsyncSession = Depends(get_session)):
        return PostDBRepository(session)

    return func


PostRepository = Annotated[PostDBRepository, Depends(get_post_repository())]
