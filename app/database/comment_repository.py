from app.database import db
from bson import ObjectId
from datetime import datetime, timezone

class CommentRepository:
    """Handles all database operations related to comments."""

    @staticmethod
    async def add_comment(article_id: str, user_id: str, content: str):
        """Insert a new comment into the database."""
        comment_data = {
            "article_id": ObjectId(article_id),
            "user_id": ObjectId(user_id),
            "content": content,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        result = await db["comments"].insert_one(comment_data)
        return result.inserted_id

    @staticmethod
    async def get_comments_by_article(article_id: str) -> list:
        """Retrieve all comments for a specific article."""

        query = {"article_id": ObjectId(article_id)}
        comments = []
        async for comment in db["comments"].find(query):
            # Convert ObjectId to string for relevant fields
            comment["_id"] = str(comment["_id"])
            comment["user_id"] = str(comment["user_id"])
            comment["article_id"] = str(comment["article_id"])
            comments.append(comment)
        return comments[:100]

    @staticmethod
    async def update_comment(comment_id: str, content: str):
        """Update an existing comment."""
        update_result = await db["comments"].update_one(
            {"_id": ObjectId(comment_id)},
            {"$set": {"content": content, "updated_at": datetime.now(timezone.utc)}}
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
