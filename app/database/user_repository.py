from app.database import db
from bson import ObjectId
from datetime import datetime

class UserRepository:
    """Handles all user-related database interactions."""

    @staticmethod
    async def find_by_email(email: str):
        """Find a user by email."""
        return await db["users"].find_one({"email": email})

    @staticmethod
    async def find_by_id(user_id: str):
        """Find a user by ID."""
        return await db["users"].find_one({"_id": ObjectId(user_id)})

    @staticmethod
    async def create_user(user_data: dict):
        """Insert a new user into the database."""
        user_data["created_at"] = datetime.utcnow()
        result = await db["users"].insert_one(user_data)
        return result.inserted_id

    @staticmethod
    async def update_user(user_id: str, update_data: dict):
        """Update a user's profile."""
        update_result = await db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data, "$currentDate": {"updated_at": True}}
        )
        return update_result.modified_count > 0  # Return True if update was successful

    @staticmethod
    async def delete_user(user_id: str):
        """Delete a user from the database."""
        delete_result = await db["users"].delete_one({"_id": ObjectId(user_id)})
        return delete_result.deleted_count > 0  # Return True if deletion was successful

    @staticmethod
    async def update_password(user_id: str, new_hashed_password: str):
        """Update a user's password."""
        update_result = await db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"hashed_password": new_hashed_password, "updated_at": datetime.utcnow()}}
        )
        return update_result.modified_count > 0
