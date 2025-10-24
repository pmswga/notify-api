import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from routers import AuthRouter, NotificationRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app=app,
        db_url="postgres://postgres:example@database:5432/notifications",
        modules={
            "models": ["models.db.notification", "models.db.user", "models.db.tokens"]
        },
        generate_schemas=True,
        _create_db=True,
    ):
        yield

    await Tortoise._drop_databases()


app = FastAPI(
    title="Notification service", lifespan=lifespan, version="0.1.0", docs_url="/docs"
)
app.include_router(router=AuthRouter)
app.include_router(router=NotificationRouter)
