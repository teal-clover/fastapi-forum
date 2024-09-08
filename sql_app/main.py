from fastapi import FastAPI, HTTPException

from . import crud, models, schemas
from .database import DBSession

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.post("/users/", status_code=201)
async def create_user(db: DBSession, user: schemas.UserCreate):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
async def read_users(db: DBSession, skip: int = 0, limit: int = 100):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: DBSession):
    db_user = await crud.get_user(db, user_id=user_id)
    return db_user


@app.put("/user/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: DBSession):
    return await crud.update_user(db=db, user=user, user_id=user_id)


@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
async def create_post_for_user(user_id: int, post: schemas.PostCreate, db: DBSession):
    return await crud.create_user_post(db=db, post=post, user_id=user_id)


@app.delete("/users/{user_id}", status_code=202)
async def delete_user(user_id: int, db: DBSession):
    await crud.delete_user(db=db, user_id=user_id)


@app.get("/posts/", response_model=list[schemas.Post])
async def read_posts(db: DBSession, skip: int = 0, limit: int = 100):
    posts = await crud.get_posts(db, skip=skip, limit=limit)
    return posts
