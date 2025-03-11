from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.base import PyObjectId

# class Article(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     title: str
#     content: str
#     tags: List[str]
#     created_at: Optional[str]
#     updated_at: Optional[str]

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
    created_at: Optional[str]
    updated_at: Optional[str]
    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
