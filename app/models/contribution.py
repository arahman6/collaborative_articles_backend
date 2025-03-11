from pydantic import BaseModel, Field
from typing import Optional
from app.models.base import PyObjectId
from datetime import datetime, timezone

class Contribution(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    article_id: str
    user: str
    content: str
    status: str = "pending"  # pending, approved, rejected
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
