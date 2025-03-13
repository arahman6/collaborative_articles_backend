# This file contains the Pydantic models for User, UserContact, UserProfessional, UserEngagement, and UserPreferences

from pydantic import BaseModel, EmailStr, Field
from app.models.base import PyObjectId
from typing import Optional, List, Dict
from datetime import datetime, timezone

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")  
    username: str  # Unique username
    email: EmailStr  # Unique email
    password: str  # Password (hashed before storing)
    profile_picture: Optional[str] = None  # Profile image URL
    bio: Optional[str] = None  # Short bio
    role: str = "contributor"  # Default role
    status: str = "active"  # Account status
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}



class UserContact(BaseModel):
    user_id: PyObjectId  # FK reference to User
    phone_number: Optional[str] = None
    alternate_email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserProfessional(BaseModel):
    user_id: PyObjectId  # FK reference to User
    job_title: Optional[str] = None
    company: Optional[str] = None
    experience_years: Optional[int] = 0
    education: Optional[List[Dict[str, str]]] = []  # List of degree info
    skills: Optional[List[str]] = []  # List of skills
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserEngagement(BaseModel):
    user_id: PyObjectId  # FK reference to User
    articles_written: int = 0
    comments_posted: int = 0
    badges: List[str] = []
    karma_score: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserPreferences(BaseModel):
    user_id: PyObjectId  # FK reference to User
    language: Optional[str] = "English"
    theme: str = "light"
    notifications: Dict[str, bool] = {"email": True, "push": False}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str