from fastapi import APIRouter, HTTPException, Depends, status
from app.database.contribution_repository import ContributionRepository
from app.database.article_repository import ArticleRepository
from app.database.user_repository import UserRepository
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
contributions_router = APIRouter()

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

@contributions_router.post("/articles/{article_id}/contribution", status_code=status.HTTP_201_CREATED)
async def log_contribution(article_id: str, action: str, current_user: dict = Depends(get_current_user)):
    """Log a user's contribution (Only for existing articles)."""
    article = await ArticleRepository.find_by_id(article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    contribution_id = await ContributionRepository.log_contribution(
        user_id=str(current_user["_id"]),
        article_id=article_id,
        action=action
    )
    return {"id": str(contribution_id), "message": f"Contribution logged: {action}"}

@contributions_router.get("/users/{user_id}/contribution", status_code=status.HTTP_200_OK)
async def get_user_contributions(user_id: str):
    """Retrieve all contributions made by a user."""
    contributions = await ContributionRepository.get_contributions_by_user(user_id)
    return contributions

@contributions_router.get("/articles/{article_id}/contribution", status_code=status.HTTP_200_OK)
async def get_article_contributions(article_id: str):
    """Retrieve all contributions made on a specific article."""
    contributions = await ContributionRepository.get_contributions_by_article(article_id)
    return contributions
