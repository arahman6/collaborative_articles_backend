from fastapi import APIRouter, HTTPException, Depends, status
from app.database.badge_repository import BadgeRepository
from app.database.user_repository import UserRepository
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
badges_router = APIRouter()

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

@badges_router.get("/assign/", status_code=status.HTTP_200_OK)
async def assign_user_badges(current_user: dict = Depends(get_current_user)):
    """Assigns badges to the user based on activity."""
    new_badges = await BadgeRepository.assign_badges(str(current_user["_id"]))
    return {"message": "Badges updated successfully", "badges": new_badges}

@badges_router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_badges(user_id: str):
    """Retrieve the badges a user has earned."""
    badges = await BadgeRepository.get_user_badges(user_id)
    return {"user_id": user_id, "badges": badges}
