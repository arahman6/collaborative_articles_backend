from app.database import db
from bson import ObjectId
from datetime import datetime

class UserActivityRepository:
    """Handles all database operations related to user activity logging."""

    @staticmethod
    async def log_activity(user_id: str, action: str, metadata: dict = None):
        """Log user activity."""
        activity_data = {
            "user_id": ObjectId(user_id),
            "action": action,  # Example: "viewed_article", "commented", "liked"
            "metadata": metadata or {},  # Additional details (e.g., article_id)
            "timestamp": datetime.utcnow()
        }
        result = await db["user_activity"].insert_one(activity_data)
        return result.inserted_id

    @staticmethod
    async def get_user_activity(user_id: str):
        """Retrieve all activity logs for a specific user."""
        return await db["user_activity"].find({"user_id": ObjectId(user_id)}).to_list(length=100)

    @staticmethod
    async def get_recent_activity(limit: int = 10):
        """Retrieve the most recent activities across all users."""
        return await db["user_activity"].find().sort("timestamp", -1).limit(limit).to_list(length=limit)
