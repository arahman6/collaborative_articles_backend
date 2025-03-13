from app.database import db
from bson import ObjectId
from datetime import datetime, timezone

class BadgeRepository:
    """Handles user badge assignments based on engagement metrics."""

    BADGE_CRITERIA = {
        "Contributor": {"articles_written": 1},
        "Commenter": {"comments_made": 5},
        "Engaged": {"articles_viewed": 10},
        "Top Contributor": {"articles_written": 5},
        "Discussion Starter": {"comments_received": 10},
        "Power User": {"articles_written": 10, "comments_made": 50, "articles_viewed": 100},
    }

    @staticmethod
    async def assign_badges(user_id: str):
        """Assigns badges based on user engagement."""
        engagement = await db["user_activity"].find({"user_id": ObjectId(user_id)}).to_list(length=100)

        # Count user actions
        articles_written = await db["articles"].count_documents({"author_id": ObjectId(user_id)})
        comments_made = await db["comments"].count_documents({"user_id": ObjectId(user_id)})
        articles_viewed = sum(1 for action in engagement if action["action"] == "viewed_article")
        comments_received = await db["comments"].count_documents({"article_id": {"$in": [doc["_id"] for doc in await db["articles"].find({"author_id": ObjectId(user_id)}).to_list(length=100)]}})

        # Determine badges
        new_badges = []
        for badge, criteria in BadgeRepository.BADGE_CRITERIA.items():
            if all(
                (criteria.get("articles_written", 0) <= articles_written) and
                (criteria.get("comments_made", 0) <= comments_made) and
                (criteria.get("articles_viewed", 0) <= articles_viewed) and
                (criteria.get("comments_received", 0) <= comments_received)
            ):
                new_badges.append(badge)

        # Store assigned badges
        await db["badges"].update_one(
            {"user_id": ObjectId(user_id)},
            {"$set": {"badges": new_badges, "updated_at": datetime.now(timezone.utc)}},
            upsert=True
        )
        return new_badges

    @staticmethod
    async def get_user_badges(user_id: str):
        """Retrieve the badges a user has earned."""
        badge_record = await db["badges"].find_one({"user_id": ObjectId(user_id)})
        return badge_record["badges"] if badge_record else []
