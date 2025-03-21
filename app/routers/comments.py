from fastapi import APIRouter, HTTPException, Depends, status
from app.database.comment_repository import CommentRepository
from app.database.article_repository import ArticleRepository
from app.database.user_repository import UserRepository
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer
from app.roles.role_factory import UserRoleFactory

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
comments_router = APIRouter()

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

@comments_router.post("/articles/{article_id}/comment", status_code=status.HTTP_201_CREATED)
async def add_comment(article_id: str, content: str, current_user: dict = Depends(get_current_user)):
    """Add a comment to an article."""
    article = await ArticleRepository.find_by_id(article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    comment_id = await CommentRepository.add_comment(
        article_id=article_id,
        user_id=str(current_user["_id"]),
        content=content
    )
    return {"id": str(comment_id), "message": "Comment added successfully"}

@comments_router.get("/articles/{article_id}/comment", status_code=status.HTTP_200_OK)
async def get_comments(article_id: str) -> list:
    """Retrieve all comments for an article."""
    print("article_id", article_id)
    comments = await CommentRepository.get_comments_by_article(article_id)
    print("comments", type(comments))
    return comments

@comments_router.put("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment(comment_id: str, content: str, current_user: dict = Depends(get_current_user)):
    """Update a comment (Only author can edit)."""
    comment = await CommentRepository.find_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if str(comment["user_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your own comments")

    success = await CommentRepository.update_comment(comment_id, content)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update comment")

    return {"message": "Comment updated successfully"}

@comments_router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a comment (Admins can delete any comment, users can delete their own)."""
    comment = await CommentRepository.find_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    user_role = UserRoleFactory.get_role(current_user["role"])
    if str(comment["user_id"]) != str(current_user["_id"]) and not user_role.can_delete_articles():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this comment")

    success = await CommentRepository.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete comment")

    return {"message": "Comment deleted successfully"}
