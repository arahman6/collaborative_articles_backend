from roles.role_interface import UserRole

class Reader(UserRole):
    """Reader role - can only view, no editing or creating."""

    def can_create_articles(self) -> bool:
        return False

    def can_edit_articles(self) -> bool:
        return False

    def can_delete_articles(self) -> bool:
        return False

    def can_manage_users(self) -> bool:
        return False
