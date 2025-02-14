from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId


# Utility to handle MongoDB's ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")
        return schema


class Article(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    tags: List[str]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "The Future of AI",
                "content": "AI is transforming the world...",
                "tags": ["AI", "Technology"],
            }
        }


class Contribution(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    article_id: str
    user: str
    content: str
    status: str = "pending"  # pending, approved, rejected
    created_at: Optional[str]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "article_id": "60d0fe4f5311236168a109ca",
                "user": "john_doe",
                "content": "I think AI ethics are crucial...",
                "status": "pending",
            }
        }


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    hashed_password: str

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "hashed_password": "hashedpassword123"
            }
        }


class Comment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    article_id: str
    user: str
    comment: str
    created_at: Optional[str]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "article_id": "60d0fe4f5311236168a109ca",
                "user": "john_doe",
                "comment": "This is an insightful article!",
                "created_at": "2023-01-01T12:00:00Z"
            }
        }




