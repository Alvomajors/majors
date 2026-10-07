from fastapi import FastAPI
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import health, items, auth
from app.blockchain import blockchain_router

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(blockchain_router, prefix="/blockchain", tags=["blockchain"])


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}"}
