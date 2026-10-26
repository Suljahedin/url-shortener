from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import health, urls


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="URL Shortener API",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(urls.router)
