from fastapi import APIRouter, HTTPException

from forum.database import DBSession
from forum.user.repository import UserRepository

from . import crud, schemas

router = APIRouter()


@router.post("/users/", status_code=201, response_model=schemas.User)
async def create_user(repo: UserRepository, user: schemas.UserCreate):
    db_user = await repo.read_one_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await repo.create(user)


@router.get("/users/", response_model=list[schemas.User])
async def read_users(repo: UserRepository, skip: int = 0, limit: int = 100):
    users = await repo.read_all(skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User, status_code=200)
async def read_user(repo: UserRepository, user_id: int):
    db_user = await repo.read_one(user_id)
    return db_user


@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(repo: UserRepository, user_id: int, user: schemas.UserUpdate):
    return await repo.update(user=user, user_id=user_id)


@router.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(repo: UserRepository, user_id: int):
    return await repo.delete(user_id=user_id)
