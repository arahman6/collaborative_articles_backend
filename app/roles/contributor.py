from app.roles.role_interface import UserRole

class Contributor(UserRole):
    """Contributor role - can create and edit, but not delete."""

    def can_create_articles(self) -> bool:
        return True

    def can_edit_articles(self) -> bool:
        return True

    def can_delete_articles(self) -> bool:
        return False

    def can_manage_users(self) -> bool:
        return False
