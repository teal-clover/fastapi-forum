from fastapi import APIRouter, HTTPException

from forum.database import DBSession

from . import crud, schemas

router = APIRouter()


@router.post("/users/{user_id}/posts/", response_model=schemas.Post, status_code=201)
async def create_post_for_user(user_id: int, post: schemas.PostCreate, db: DBSession):
    return await crud.create_user_post(db=db, post=post, user_id=user_id)


@router.get("/posts/", response_model=list[schemas.Post])
async def read_posts(db: DBSession, skip: int = 0, limit: int = 100):
    posts = await crud.get_posts(db, skip=skip, limit=limit)
    return posts
