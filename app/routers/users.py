from fastapi import APIRouter, HTTPException, Depends, status
from app.database.user_repository import UserRepository
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.services.auth_service import AuthService
from pydantic import BaseModel
from app.roles.role_factory import UserRoleFactory

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users_router = APIRouter()

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Retrieve the currently authenticated user from JWT."""
    try:
        payload = AuthService.decode_access_token(token)
        user_email: str = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = await UserRepository.find_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

@users_router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def signup(user: User):
    """Registers a new user."""
    user_data = user.model_dump()  
    user_data["hashed_password"] = AuthService.hash_password(user_data.pop("password"))  # Hash password
    
    existing_user = await UserRepository.find_by_email(user_data["email"])
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = await UserRepository.create_user(user_data)
    return {"id": str(user_id), "email": user.email}

@users_router.post("/login/", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates a user and returns JWT token."""
    user = await UserRepository.find_by_email(form_data.username)

    if not user or not AuthService.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = AuthService.create_access_token({"sub": user["email"]})
    
    return {"access_token": access_token, "token_type": "bearer"}

@users_router.get("/profile/", status_code=status.HTTP_200_OK)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Retrieve the profile of the logged-in user."""
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

@users_router.put("/profile/", status_code=status.HTTP_200_OK)
async def update_profile(update_data: dict, current_user: dict = Depends(get_current_user)):
    """Update user profile."""
    success = await UserRepository.update_user(str(current_user["_id"]), update_data)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No changes made")
    
    return {"message": "Profile updated successfully"}

@users_router.put("/change-password/", status_code=status.HTTP_200_OK)
async def change_password(request: ChangePasswordRequest, current_user: dict = Depends(get_current_user)):
    """Change user's password."""
    if not AuthService.verify_password(request.old_password, current_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

    new_hashed_password = AuthService.hash_password(request.new_password)
    success = await UserRepository.update_password(str(current_user["_id"]), new_hashed_password)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update password")

    return {"message": "Password changed successfully"}

@users_router.delete("/delete-account/", status_code=status.HTTP_200_OK)
async def delete_account(current_user: dict = Depends(get_current_user)):
    """Delete user account."""
    success = await UserRepository.delete_user(str(current_user["_id"]))

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete account")

    return {"message": "Account deleted successfully"}

@users_router.get("/manage-users/", status_code=status.HTTP_200_OK)
async def manage_users(current_user: dict = Depends(get_current_user)):
    """Only Admins can manage users."""
    user_role = UserRoleFactory.get_role(current_user["role"])
    if not user_role.can_manage_users():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to manage users")
    
    return {"message": "You have admin privileges."}

@users_router.delete("/delete-article/{article_id}", status_code=status.HTTP_200_OK)
async def delete_article(article_id: str, current_user: dict = Depends(get_current_user)):
    """Only Admins can delete articles."""
    user_role = UserRoleFactory.get_role(current_user["role"])
    if not user_role.can_delete_articles():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete articles")
    
    return {"message": f"Article {article_id} deleted successfully"}
