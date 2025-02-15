from pydantic import BaseModel, Field
from typing import Optional
from app.models.base import PyObjectId

class Comment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    article_id: str
    user: str
    comment: str
    created_at: Optional[str]

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
        json_schema_extra = {
            "example": {
                "article_id": "60d0fe4f5311236168a109ca",
                "user": "john_doe",
                "comment": "This is an insightful article!",
                "created_at": "2023-01-01T12:00:00Z"
            }
        }
