from fastapi import APIRouter, HTTPException, Depends, status
from app.database.admin_repository import AdminRepository
from app.database.user_repository import UserRepository
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer
from roles.role_factory import UserRoleFactory

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
admin_router = APIRouter()

async def get_current_admin(token: str = Depends(oauth2_scheme)):
    """Retrieve the currently authenticated admin user from JWT."""
    try:
        payload = AuthService.decode_access_token(token)
        user_email: str = payload.get("sub")
        user = await UserRepository.find_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_role = UserRoleFactory.get_role(user["role"])
        if user_role.__class__.__name__ != "Admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access restricted to admins")

        return user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

@admin_router.get("/moderation-queue/", status_code=status.HTTP_200_OK)
async def get_pending_articles(current_admin: dict = Depends(get_current_admin)):
    """Retrieve all articles pending admin approval."""
    pending_articles = await AdminRepository.get_moderation_queue()
    return pending_articles

@admin_router.post("/approve-article/{article_id}", status_code=status.HTTP_200_OK)
async def approve_article(article_id: str, current_admin: dict = Depends(get_current_admin)):
    """Approve a pending article."""
    success = await AdminRepository.approve_article(article_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Article approval failed")

    return {"message": "Article approved successfully"}

@admin_router.delete("/delete-article/{article_id}", status_code=status.HTTP_200_OK)
async def delete_article(article_id: str, current_admin: dict = Depends(get_current_admin)):
    """Delete an article."""
    success = await AdminRepository.delete_article(article_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete article")

    return {"message": "Article deleted successfully"}

@admin_router.get("/flagged-comments/", status_code=status.HTTP_200_OK)
async def get_flagged_comments(current_admin: dict = Depends(get_current_admin)):
    """Retrieve flagged comments for review."""
    flagged_comments = await AdminRepository.get_flagged_comments()
    return flagged_comments

@admin_router.delete("/delete-comment/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: str, current_admin: dict = Depends(get_current_admin)):
    """Delete a flagged comment."""
    success = await AdminRepository.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete comment")

    return {"message": "Comment deleted successfully"}

@admin_router.post("/ban-user/{user_id}", status_code=status.HTTP_200_OK)
async def ban_user(user_id: str, current_admin: dict = Depends(get_current_admin)):
    """Ban a user."""
    success = await AdminRepository.ban_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to ban user")

    return {"message": "User banned successfully"}

@admin_router.post("/restore-user/{user_id}", status_code=status.HTTP_200_OK)
async def restore_user(user_id: str, current_admin: dict = Depends(get_current_admin)):
    """Restore a banned user."""
    success = await AdminRepository.restore_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to restore user")

    return {"message": "User restored successfully"}
