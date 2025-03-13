from app.database import db
from bson import ObjectId
from datetime import datetime, timezone

class ContributionRepository:
    """Handles all database operations related to contributions."""

    @staticmethod
    async def log_contribution(user_id: str, article_id: str, action: str):
        """Log a user's contribution to an article."""
        contribution_data = {
            "user_id": ObjectId(user_id),
            "article_id": ObjectId(article_id),
            "action": action,  # 'created', 'edited'
            "timestamp": datetime.now(timezone.utc)
        }
        result = await db["contributions"].insert_one(contribution_data)
        return result.inserted_id

    @staticmethod
    async def get_contributions_by_user(user_id: str):
        """Retrieve all contributions made by a specific user."""
        return await db["contributions"].find({"user_id": ObjectId(user_id)}).to_list(length=100)

    @staticmethod
    async def get_contributions_by_article(article_id: str):
        """Retrieve all contributions made on a specific article."""
        return await db["contributions"].find({"article_id": ObjectId(article_id)}).to_list(length=100)
