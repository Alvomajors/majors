from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import health, items, auth
from app.blockchain import blockchain_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-ready Majors API with MongoDB, JWT auth, and Ethereum integration.",
    lifespan=lifespan,
)

app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(blockchain_router, prefix="/blockchain", tags=["blockchain"])


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}"}
