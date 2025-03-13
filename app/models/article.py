from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.base import PyObjectId
from datetime import datetime, timezone
class AuthorModel(BaseModel):
    name: str
    avatar: str

class Article(BaseModel):
    id: str = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    img: str
    tag: List[str] = []
    authors: List[AuthorModel] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
