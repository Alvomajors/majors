from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

from app.database import get_database

router = APIRouter()


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = 0.0


class ItemResponse(ItemCreate):
    id: str


@router.get("/", response_model=list[ItemResponse])
async def list_items():
    db = await get_database()
    items = []
    async for item in db.items.find():
        item["id"] = str(item.pop("_id"))
        items.append(item)
    return items


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    db = await get_database()
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item["id"] = str(item.pop("_id"))
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    db = await get_database()
    created = await db.items.insert_one(item.dict())
    saved_item = await db.items.find_one({"_id": created.inserted_id})
    saved_item["id"] = str(saved_item.pop("_id"))
    return saved_item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemCreate):
    db = await get_database()
    updated = await db.items.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict()},
        return_document=True,
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Item not found")
    updated["id"] = str(updated.pop("_id"))
    return updated


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    db = await get_database()
    result = await db.items.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
