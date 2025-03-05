from abc import ABC, abstractmethod

class UserRole(ABC):
    """Abstract base class for user roles."""

    @abstractmethod
    def can_create_articles(self) -> bool:
        pass

    @abstractmethod
    def can_edit_articles(self) -> bool:
        pass

    @abstractmethod
    def can_delete_articles(self) -> bool:
        pass

    @abstractmethod
    def can_manage_users(self) -> bool:
        pass
