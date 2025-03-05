from app.database import db
from bson import ObjectId
from datetime import datetime

class CommentRepository:
    """Handles all database operations related to comments."""

    @staticmethod
    async def add_comment(article_id: str, user_id: str, content: str):
        """Insert a new comment into the database."""
        comment_data = {
            "article_id": ObjectId(article_id),
            "user_id": ObjectId(user_id),
            "content": content,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = await db["comments"].insert_one(comment_data)
        return result.inserted_id

    @staticmethod
    async def get_comments_by_article(article_id: str):
        """Retrieve all comments for a specific article."""
        return await db["comments"].find({"article_id": ObjectId(article_id)}).to_list(length=100)

    @staticmethod
    async def update_comment(comment_id: str, content: str):
        """Update an existing comment."""
        update_result = await db["comments"].update_one(
            {"_id": ObjectId(comment_id)},
            {"$set": {"content": content, "updated_at": datetime.utcnow()}}
        )
        return update_result.modified_count > 0  # True if updated successfully

    @staticmethod
    async def delete_comment(comment_id: str):
        """Delete a comment from the database."""
        delete_result = await db["comments"].delete_one({"_id": ObjectId(comment_id)})
        return delete_result.deleted_count > 0  # True if deleted successfully

    @staticmethod
    async def find_comment_by_id(comment_id: str):
        """Find a comment by its ID."""
        return await db["comments"].find_one({"_id": ObjectId(comment_id)})
