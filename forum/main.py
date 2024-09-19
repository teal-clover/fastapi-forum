from fastapi import FastAPI

from forum.post.router import router as post_router
from forum.user.router import router as user_router

app = FastAPI()


app.include_router(user_router)
app.include_router(post_router)
