from roles.role_interface import UserRole

class Admin(UserRole):
    """Admin role - has full permissions."""

    def can_create_articles(self) -> bool:
        return True

    def can_edit_articles(self) -> bool:
        return True

    def can_delete_articles(self) -> bool:
        return True

    def can_manage_users(self) -> bool:
        return True
