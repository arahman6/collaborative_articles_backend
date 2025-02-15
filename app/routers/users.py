from fastapi import APIRouter, HTTPException, Depends
from app.database import db
from app.models import User
from datetime import datetime, timezone
from bson import ObjectId
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.config import config

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT settings
SECRET_KEY = config.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# User Authentication Router
users_router = APIRouter()

@users_router.post("/signup/")
async def signup(user: User):
    user_data = user.dict()
    user_data["password"] = get_password_hash(user_data["password"])
    existing_user = await db["users"].find_one({"email": user_data["email"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data["created_at"] = datetime.now(timezone.utc)
    result = await db["users"].insert_one(user_data)
    return {"id": str(result.inserted_id), "email": user.email}

@users_router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db["users"].find_one({"email": form_data.email})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

