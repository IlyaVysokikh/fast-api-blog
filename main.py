from fastapi import FastAPI

from src.routers import user, posts

app = FastAPI()

app.include_router(user.router, prefix="")
app.include_router(posts.router, prefix="")
