from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Comment
from datetime import datetime, timezone
from bson import ObjectId

comments_router = APIRouter()

# Create a new comment
@comments_router.post("/comments/")
async def add_comment(article_id: str, comment: Comment):
    comment_data = comment.dict()
    comment_data["article_id"] = article_id
    comment_data["created_at"] = datetime.now(timezone.utc)
    result = await db["comments"].insert_one(comment_data)
    return {"id": str(result.inserted_id)}

# Get all comments
@comments_router.get("/comments/")
async def get_comments():
    comments = await db["comments"].find().to_list(100)
    for comment in comments:
        comment["_id"] = str(comment["_id"])
    return comments

# Get a single comment by ID
@comments_router.get("/comments/{comment_id}")
async def get_comment(comment_id: str):
    comment = await db["comments"].find_one({"_id": ObjectId(comment_id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment["_id"] = str(comment["_id"])
    return comment

# Update a comment by ID
@comments_router.put("/comments/{comment_id}")
async def update_comment(comment_id: str, comment: Comment):
    comment_data = comment.dict(exclude_unset=True)
    comment_data["updated_at"] = datetime.now(timezone.utc)
    result = await db["comments"].update_one({"_id": ObjectId(comment_id)}, {"$set": comment_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Comment not found or no changes made")
    return {"message": "Comment updated successfully"}

# Delete a comment by ID
@comments_router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: str):
    result = await db["comments"].delete_one({"_id": ObjectId(comment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
