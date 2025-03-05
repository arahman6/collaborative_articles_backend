from fastapi import APIRouter, HTTPException, Depends, status
from app.database.article_repository import ArticleRepository
from app.database.comment_repository import CommentRepository
from app.database.contribution_repository import ContributionRepository
from app.database.user_activity_repository import UserActivityRepository
from app.models.article import Article
from app.database.user_repository import UserRepository
from app.services.article_generator_service import ArticleGeneratorService
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer
from app.roles.role_factory import UserRoleFactory

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
articles_router = APIRouter()

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

async def get_current_user_email(token: str = Depends(oauth2_scheme)):
    """Retrieve the email of the authenticated user from JWT (no DB call)."""
    try:
        payload = AuthService.decode_access_token(token)
        user_email: str = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_email
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


@articles_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article(article: Article, current_user: dict = Depends(get_current_user)):
    """Create a new article (Only Admins & Contributors)."""
    user_role = UserRoleFactory.get_role(current_user["role"])
    if not user_role.can_create_articles():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to create articles")

    article_data = article.model_dump()
    article_data["author_id"] = str(current_user["_id"])
    article_id = await ArticleRepository.create_article(article_data)

    # Automatically Log Contribution
    await ContributionRepository.log_contribution(
        user_id=str(current_user["_id"]),
        article_id=str(article_id),
        action="created"
    )

    return {"id": str(article_id), "message": "Article created successfully"}

@articles_router.get("/{article_id}", status_code=status.HTTP_200_OK)
async def get_article(article_id: str, current_user: dict = Depends(get_current_user)):
    """Retrieve an article and log that the user viewed it."""
    article = await ArticleRepository.find_by_id(article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    # Log user activity
    await UserActivityRepository.log_activity(
        user_id=str(current_user["_id"]),
        action="viewed_article",
        metadata={"article_id": article_id}
    )

    return article

@articles_router.put("/{article_id}", status_code=status.HTTP_200_OK)
async def update_article(article_id: str, update_data: dict, current_user: dict = Depends(get_current_user)):
    """Update an article (Only Admins & Contributors)."""
    user_role = UserRoleFactory.get_role(current_user["role"])
    if not user_role.can_edit_articles():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to edit articles")

    success = await ArticleRepository.update_article(article_id, update_data)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update article")

    # Automatically Log Contribution
    await ContributionRepository.log_contribution(
        user_id=str(current_user["_id"]),
        article_id=article_id,
        action="edited"
    )

    return {"message": "Article updated successfully"}

@articles_router.delete("/{article_id}", status_code=status.HTTP_200_OK)
async def delete_article(article_id: str, current_user: dict = Depends(get_current_user)):
    """Delete an article (Only Admins)."""
    user_role = UserRoleFactory.get_role(current_user["role"])
    if not user_role.can_delete_articles():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete articles")

    success = await ArticleRepository.delete_article(article_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete article")

    return {"message": "Article deleted successfully"}

@articles_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_articles():
    """Retrieve all articles."""
    articles = await ArticleRepository.get_all_articles()
    return articles

@articles_router.post("/{article_id}/comment", status_code=status.HTTP_201_CREATED)
async def add_comment(article_id: str, content: str, current_user: dict = Depends(get_current_user)):
    """Add a comment and notify the article author."""
    article = await ArticleRepository.find_by_id(article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    comment_id = await CommentRepository.add_comment(
        article_id=article_id,
        user_id=str(current_user["_id"]),
        content=content
    )

    # Notify the author
    author = await UserRepository.find_by_id(str(article["author_id"]))
    if author:
        print(f"Notification: {author['email']} - Your article has a new comment!")

    return {"id": str(comment_id), "message": "Comment added successfully"}

@articles_router.post("/generate/", status_code=201)
async def generate_articles(current_user: dict = Depends(get_current_user)):
    """Generates AI articles (Only Admins)."""
    user_role = UserRoleFactory.get_role(current_user["role"])
    if not user_role.can_create_articles():
        raise HTTPException(status_code=403, detail="You do not have permission to generate articles")

    response = await ArticleGeneratorService.generate_and_save_articles()
    return response
