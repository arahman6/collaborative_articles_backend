from fastapi import APIRouter, HTTPException, Depends, status
from app.database.user_activity_repository import UserActivityRepository
from app.database.user_repository import UserRepository
from app.database.badge_repository import BadgeRepository
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_activity_router = APIRouter()

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

@user_activity_router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_activity(user_id: str):
    """Retrieve all activity logs for a specific user."""
    activity_logs = await UserActivityRepository.get_user_activity(user_id)
    return activity_logs

@user_activity_router.get("/recent/", status_code=status.HTTP_200_OK)
async def get_recent_activity(limit: int = 10):
    """Retrieve the most recent user activities."""
    recent_activity = await UserActivityRepository.get_recent_activity(limit)
    return recent_activity


@user_activity_router.post("/log/", status_code=status.HTTP_201_CREATED)
async def log_user_activity(action: str, metadata: dict = None, current_user: dict = Depends(get_current_user)):
    """Logs user activity and updates badges."""
    activity_id = await UserActivityRepository.log_activity(
        user_id=str(current_user["_id"]),
        action=action,
        metadata=metadata
    )

    # Automatically update badges
    await BadgeRepository.assign_badges(str(current_user["_id"]))

    return {"message": f"Activity logged: {action}", "activity_id": str(activity_id)}
