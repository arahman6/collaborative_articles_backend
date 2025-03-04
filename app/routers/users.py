from fastapi import APIRouter, HTTPException, Depends, status
from app.database import db
from app.models.user import ChangePasswordRequest, User
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.config import config

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT settings
SECRET_KEY = str(config.JWT_SECRET_KEY) 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# User Router
users_router = APIRouter()

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generate JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Retrieve the currently authenticated user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = await db["users"].find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

# User Signup
@users_router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def signup(user: User):
    """Register a new user"""
    user_data = user.model_dump()  
    user_data["hashed_password"] = get_password_hash(user_data.pop("password"))  # Hash password
    
    existing_user = await db["users"].find_one({"email": user_data["email"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data["created_at"] = datetime.now(timezone.utc)
    result = await db["users"].insert_one(user_data)
    
    return {"id": str(result.inserted_id), "email": user.email}

# User Login & Token Generation
@users_router.post("/login/", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token"""
    user = await db["users"].find_one({"email": form_data.username})

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": user["email"]})
    
    return {"access_token": access_token, "token_type": "bearer"}

# Get Current User Profile
@users_router.get("/profile/", status_code=status.HTTP_200_OK)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Retrieve the profile of the logged-in user"""
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "email": current_user["email"],
        "profile_picture": current_user.get("profile_picture", None),
        "bio": current_user.get("bio", ""),
        "role": current_user.get("role", "contributor"),
        "status": current_user.get("status", "active"),
        "created_at": current_user.get("created_at")
    }

# Update User Profile
@users_router.put("/profile/", status_code=status.HTTP_200_OK)
async def update_profile(update_data: dict, current_user: dict = Depends(get_current_user)):
    """Update user profile"""
    update_result = await db["users"].update_one(
        {"_id": current_user["_id"]},
        {"$set": update_data, "$currentDate": {"updated_at": True}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No changes made")
    
    return {"message": "Profile updated successfully"}

# Change Password
@users_router.put("/change-password/", status_code=200)
async def change_password(
    request: ChangePasswordRequest, 
    current_user: dict = Depends(get_current_user)
):
    """Change user's password"""
    if not verify_password(request.old_password, current_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    new_hashed_password = get_password_hash(request.new_password)
    await db["users"].update_one(
        {"_id": current_user["_id"]},
        {"$set": {"hashed_password": new_hashed_password}}
    )

    return {"message": "Password changed successfully"}


# Delete User Account
@users_router.delete("/delete-account/", status_code=status.HTTP_200_OK)
async def delete_account(current_user: dict = Depends(get_current_user)):
    """Delete user account"""
    delete_result = await db["users"].delete_one({"_id": current_user["_id"]})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete account")

    return {"message": "Account deleted successfully"}
