from fastapi import APIRouter, HTTPException

from forum.database import DBSession

from . import crud, schemas

router = APIRouter()


@router.post("/users/", status_code=201)
async def create_user(db: DBSession, user: schemas.UserCreate):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
async def read_users(db: DBSession, skip: int = 0, limit: int = 100):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: DBSession):
    db_user = await crud.get_user(db, user_id=user_id)
    return db_user


@router.put("/user/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: DBSession):
    return await crud.update_user(db=db, user=user, user_id=user_id)


@router.delete("/users/{user_id}", status_code=202)
async def delete_user(user_id: int, db: DBSession):
    await crud.delete_user(db=db, user_id=user_id)
