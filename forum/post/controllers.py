from forum.base.exceptions import PostNotFoundException
from forum.post import models, schemas
from forum.post.repository import PostRepository
from forum.user.models import User


class PostController:
    def __init__(
        self,
        repo: PostRepository,
    ):
        self.repo = repo

    async def create(self, post: schemas.PostCreate, user: User) -> models.Post:
        post = await self.repo.create(item=post, user_id=int(user.id))
        return post

    async def read_all(self, skip: int = 0, limit: int = 100) -> list[models.Post]:
        posts = await self.repo.read_all(skip=skip, limit=limit)
        return posts

    async def read_one(self, post_id: int) -> models.Post:
        post = await self.repo.read_one(post_id)
        if not post:
            raise PostNotFoundException
        return post

    async def update(self, post_id: int, post: schemas.PostUpdate) -> models.Post:
        post = await self.repo.update(post_id, post)
        if not post:
            raise PostNotFoundException
        return post

    async def delete(self, post_id: int) -> models.Post:
        post = await self.repo.delete(post_id)
        if not post:
            raise PostNotFoundException
        return post
