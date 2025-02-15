from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Contribution
from datetime import datetime, timezone
from bson import ObjectId

contributions_router = APIRouter()

# Create a new contribution
@contributions_router.post("/contributions/")
async def add_contribution(article_id: str, contribution: Contribution):
    contribution_data = contribution.dict()
    contribution_data["article_id"] = article_id
    contribution_data["created_at"] = datetime.now(timezone.utc)
    result = await db["contributions"].insert_one(contribution_data)
    return {"id": str(result.inserted_id)}

# Get all contributions
@contributions_router.get("/contributions/")
async def get_contributions():
    contributions = await db["contributions"].find().to_list(100)
    for contribution in contributions:
        contribution["_id"] = str(contribution["_id"])
    return contributions

# Get a single contribution by ID
@contributions_router.get("/contributions/{contribution_id}")
async def get_contribution(contribution_id: str):
    contribution = await db["contributions"].find_one({"_id": ObjectId(contribution_id)})
    if not contribution:
        raise HTTPException(status_code=404, detail="Contribution not found")
    contribution["_id"] = str(contribution["_id"])
    return contribution

# Update a contribution by ID
@contributions_router.put("/contributions/{contribution_id}")
async def update_contribution(contribution_id: str, contribution: Contribution):
    contribution_data = contribution.dict(exclude_unset=True)
    contribution_data["updated_at"] = datetime.now(timezone.utc)
    result = await db["contributions"].update_one({"_id": ObjectId(contribution_id)}, {"$set": contribution_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Contribution not found or no changes made")
    return {"message": "Contribution updated successfully"}

# Delete a contribution by ID
@contributions_router.delete("/contributions/{contribution_id}")
async def delete_contribution(contribution_id: str):
    result = await db["contributions"].delete_one({"_id": ObjectId(contribution_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return {"message": "Contribution deleted successfully"}