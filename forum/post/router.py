from fastapi import APIRouter, HTTPException

from forum.database import DBSession
from forum.post.repository import PostRepository

from . import crud, schemas

router = APIRouter()


@router.post("/users/{user_id}/posts/", response_model=schemas.Post, status_code=201)
async def create_post_for_user(repo: PostRepository, user_id: int, post: schemas.PostCreate):
    return await repo.create(post=post, user_id=user_id)


@router.get("/posts/", response_model=list[schemas.Post])
async def read_posts(repo: PostRepository, skip: int = 0, limit: int = 100):
    posts = await repo.read_all(skip=skip, limit=limit)
    return posts
