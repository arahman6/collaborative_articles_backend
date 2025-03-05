from roles.admin import Admin
from roles.contributor import Contributor
from roles.reader import Reader

class UserRoleFactory:
    """Factory to return role classes based on user role string."""

    @staticmethod
    def get_role(role: str):
        role_mapping = {
            "admin": Admin(),
            "contributor": Contributor(),
            "reader": Reader()
        }
        return role_mapping.get(role.lower(), Reader())  # Default to Reader if role is unknown
