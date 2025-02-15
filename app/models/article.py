from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.base import PyObjectId

class Article(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    tags: List[str]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "The Future of AI",
                "content": "AI is transforming the world...",
                "tags": ["AI", "Technology"],
            }
        }
