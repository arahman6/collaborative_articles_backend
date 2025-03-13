from fastapi import APIRouter, HTTPException, Depends, status
from app.database.engagement_analytics_repository import EngagementAnalyticsRepository
from app.database.user_repository import UserRepository
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer
from roles.role_factory import UserRoleFactory

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
engagement_analytics_router = APIRouter()

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

@engagement_analytics_router.get("/top-users/", status_code=status.HTTP_200_OK)
async def get_most_active_users(limit: int = 5, current_user: dict = Depends(get_current_user)):
    """Retrieve the most active users (Admins only)."""
    user_role = UserRoleFactory.get_role(current_user["role"])
    if not user_role.can_manage_users():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view analytics")

    top_users = await EngagementAnalyticsRepository.get_most_active_users(limit)
    return top_users

@engagement_analytics_router.get("/top-articles/", status_code=status.HTTP_200_OK)
async def get_most_viewed_articles(limit: int = 5):
    """Retrieve the most viewed articles."""
    top_articles = await EngagementAnalyticsRepository.get_most_viewed_articles(limit)
    return top_articles

@engagement_analytics_router.get("/most-commented/", status_code=status.HTTP_200_OK)
async def get_most_commented_articles(limit: int = 5):
    """Retrieve the most commented articles."""
    most_commented = await EngagementAnalyticsRepository.get_most_commented_articles(limit)
    return most_commented

@engagement_analytics_router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_engagement(user_id: str):
    """Retrieve a user's total contributions (articles + comments)."""
    engagement = await EngagementAnalyticsRepository.get_user_engagement(user_id)
    return engagement
