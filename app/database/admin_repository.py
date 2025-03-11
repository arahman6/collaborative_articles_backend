from app.database import db
from bson import ObjectId
from datetime import datetime, timezone

class AdminRepository:
    """Handles admin actions like content moderation and user management."""

    @staticmethod
    async def approve_article(article_id: str):
        """Approve a submitted article."""
        update_result = await db["articles"].update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {"status": "approved", "updated_at": datetime.now(timezone.utc)}}
        )
        return update_result.modified_count > 0

    @staticmethod
    async def delete_article(article_id: str):
        """Delete an article."""
        delete_result = await db["articles"].delete_one({"_id": ObjectId(article_id)})
        return delete_result.deleted_count > 0

    @staticmethod
    async def delete_comment(comment_id: str):
        """Delete an inappropriate comment."""
        delete_result = await db["comments"].delete_one({"_id": ObjectId(comment_id)})
        return delete_result.deleted_count > 0

    @staticmethod
    async def ban_user(user_id: str):
        """Ban a user from the platform."""
        update_result = await db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"status": "banned", "updated_at": datetime.now(timezone.utc)}}
        )
        return update_result.modified_count > 0

    @staticmethod
    async def restore_user(user_id: str):
        """Restore a banned user."""
        update_result = await db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"status": "active", "updated_at": datetime.now(timezone.utc)}}
        )
        return update_result.modified_count > 0

    @staticmethod
    async def get_moderation_queue():
        """Retrieve all pending articles for approval."""
        return await db["articles"].find({"status": "pending"}).to_list(length=100)

    @staticmethod
    async def get_flagged_comments():
        """Retrieve flagged comments that need moderation."""
        return await db["comments"].find({"status": "flagged"}).to_list(length=100)
