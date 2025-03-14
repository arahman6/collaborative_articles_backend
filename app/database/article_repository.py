from app.database import db
from bson import ObjectId
from datetime import datetime, timezone

class ArticleRepository:
    """Handles all database operations related to articles."""

    @staticmethod
    async def create_article(article_data: dict):
        """Insert a new article into the database."""
        article_data["created_at"] = datetime.now(timezone.utc)
        article_data["updated_at"] = datetime.now(timezone.utc)
        result = await db["articles"].insert_one(article_data)
        return result.inserted_id

    @staticmethod
    async def bulk_insert_articles(articles_data: list):
        """Insert multiple articles into the database."""
        if not articles_data:
            return
        await db["articles"].insert_many(articles_data)

    @staticmethod
    async def find_by_id(article_id: str):
        """Find an article by ID."""
        try:
            object_id = ObjectId(article_id)  
        except:
            raise ValueError("Invalid article ID format")
        return await db["articles"].find_one({"_id": ObjectId(article_id)})

    @staticmethod
    async def update_article(article_id: str, update_data: dict):
        """Update an existing article."""
        update_result = await db["articles"].update_one(
            {"_id": ObjectId(article_id)},
            {"$set": update_data, "$currentDate": {"updated_at": True}}
        )
        return update_result.modified_count > 0  # Return True if updated successfully

    @staticmethod
    async def delete_article(article_id: str):
        """Delete an article from the database."""
        delete_result = await db["articles"].delete_one({"_id": ObjectId(article_id)})
        return delete_result.deleted_count > 0  # Return True if deleted successfully

    @staticmethod
    async def get_all_articles():
        """Retrieve all articles."""
        return await db["articles"].find().sort("created_at", -1).to_list(length=100)
