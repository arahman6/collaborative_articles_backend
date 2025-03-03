from pydantic import BaseModel, EmailStr, Field
from app.models.base import PyObjectId
from typing import Optional

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")  # MongoDB ID
    username: str  # Ensure username is included
    email: EmailStr  # Ensures a valid email format
    password: str  # Keep `password` for signup (will be hashed later)

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "securepassword123"
            }
        }
