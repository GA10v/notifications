from uuid import UUID
from services.generator.src.service.connector import AuthenticatedSession


class UGCConnection:
    def __init__(self, connector: AuthenticatedSession):
        self.connector = connector

    def get_users_for_new_content(self, movie_id: UUID) -> list[str]:
        """Return list of users, subscribed to new content events."""
        return self.connector.get(url=f'/ugc/v1/subscribers/{movie_id}')


class AuthConnection:
    def __init__(self, connector: AuthenticatedSession):
        self.connector = connector

    def get_user_data(self, user_id: UUID) -> list[str]:
        """Return list of users, subscribed to new content events."""
        ...