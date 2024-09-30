from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from forum.base.database import create_db
from forum.base.exceptions import CredentialsException
from forum.comment.router import router as comment_router
from forum.post.router import router as post_router
from forum.user.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(CredentialsException)
async def unicorn_exception_handler(request: Request, exc: CredentialsException):
    return JSONResponse(
        status_code=403,
        content={"message": "Check your credentials."},
    )


app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
