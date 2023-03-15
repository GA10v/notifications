import os
from contextlib import closing

import psycopg2
from psycopg2.extras import DictCursor

from admin_panel.generator.src.models.notifications import Event
from admin_panel.generator.src.models.user import User
from admin_panel.generator.src.service.connector import AuthenticatedSession

db_creds = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432),
}


class UGCConnection:
    def __init__(self, connector: AuthenticatedSession):
        self.connector = connector

    def get_content_subscribers(self, content_id: str) -> list[str]:
        """Return list of users, subscribed to new content events."""
        return self.connector.get(url=f'/ugc/v1/subscribers/{content_id}')

    def get_likes_count(self, review_id: str) -> int:
        """Return number of current likes on review."""
        return self.connector.get(url=f'/ugc/v1/likes_count/{review_id}')

    def close(self) -> None:
        """Close requests session."""
        self.connector.close()


class AuthConnection:
    def __init__(self, connector: AuthenticatedSession):
        self.connector = connector

    def get_user_data(self, user_id: str) -> User:
        """Return list of users, subscribed to new content events."""
        response = self.connector.get(url=f'/auth/v1/user_info/{user_id}')
        return response if response.ok else response.raise_for_status()

    def get_user_group(self, group_id: str) -> list[str]:
        """Return list of users, belong to the group."""
        response = self.connector.get(url=f'/auth/v1/user_group/{group_id}')
        return response if response.ok else response.raise_for_status()

    def filter_users(self, user_ids: list[str], conditions: list) -> list[str]:
        """Filter users, that match the conditions."""
        return [self.get_user_data(user_id).user_id for user_id in user_ids if conditions]

    def close(self) -> None:
        """Close requests session."""
        self.connector.close()


class ApiConnection:
    def __init__(self, connector: AuthenticatedSession):
        self.connector = connector

    def send_event(self, event: Event):
        response = self.connector.post(url='/test_new_content', payload=event)
        return response if response.ok else response.raise_for_status()

    def close(self) -> None:
        """Close requests session."""
        self.connector.close()


class PGConnection:
    def __init__(self):
        with closing(psycopg2.connect(**db_creds)) as pg_conn:
            self.cursor = pg_conn.cursor(cursor_factory=DictCursor)

    def fetch_table(self, command: str) -> list[dict]:
        """Get data from table."""
        self.cursor.execute(command)
        data = self.cursor.fetchall()
        return [dict(el) for el in data]
