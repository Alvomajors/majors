from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI(title="Majors API")

MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://root:password123@localhost:27017/majors?authSource=admin",
)

client = MongoClient(MONGODB_URL)
db = client["majors"]

@app.get("/")
def read_root():
    return {"message": "Majors API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/items")
def create_item(item: dict):
    result = db.items.insert_one(item)
    return {"id": str(result.inserted_id), "item": item}

@app.get("/items")
def get_items():
    items = list(db.items.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return {"items": items}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
