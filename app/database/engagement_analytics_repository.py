from app.database import db
from bson import ObjectId

class EngagementAnalyticsRepository:
    """Handles user engagement analytics queries."""

    @staticmethod
    async def get_most_active_users(limit: int = 5):
        """Retrieve the top users based on activity count."""
        pipeline = [
            {"$group": {"_id": "$user_id", "activity_count": {"$sum": 1}}},
            {"$sort": {"activity_count": -1}},
            {"$limit": limit}
        ]
        return await db["user_activity"].aggregate(pipeline).to_list(length=limit)

    @staticmethod
    async def get_most_viewed_articles(limit: int = 5):
        """Retrieve the top viewed articles."""
        pipeline = [
            {"$match": {"action": "viewed_article"}},
            {"$group": {"_id": "$metadata.article_id", "view_count": {"$sum": 1}}},
            {"$sort": {"view_count": -1}},
            {"$limit": limit}
        ]
        return await db["user_activity"].aggregate(pipeline).to_list(length=limit)

    @staticmethod
    async def get_most_commented_articles(limit: int = 5):
        """Retrieve the most commented articles."""
        pipeline = [
            {"$group": {"_id": "$article_id", "comment_count": {"$sum": 1}}},
            {"$sort": {"comment_count": -1}},
            {"$limit": limit}
        ]
        return await db["comments"].aggregate(pipeline).to_list(length=limit)

    @staticmethod
    async def get_user_engagement(user_id: str):
        """Retrieve a user's total contributions and comments."""
        articles_written = await db["articles"].count_documents({"author_id": ObjectId(user_id)})
        comments_made = await db["comments"].count_documents({"user_id": ObjectId(user_id)})

        return {
            "user_id": user_id,
            "articles_written": articles_written,
            "comments_made": comments_made
        }
