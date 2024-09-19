from typing import Annotated

from fastapi import APIRouter, Depends

from forum.post.controllers import PostController
from forum.post.repository import PostRepository

from . import schemas

router = APIRouter()


@router.post("/posts/", response_model=schemas.Post, status_code=201)
async def create_post_for_user(controller: Annotated[PostController, Depends()], post: schemas.PostCreate):
    return await controller.create(post=post)


@router.get("/posts/", response_model=list[schemas.Post])
async def read_posts(repo: PostRepository, skip: int = 0, limit: int = 100):
    posts = await repo.read_all(skip=skip, limit=limit)
    return posts
