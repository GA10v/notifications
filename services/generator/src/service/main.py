from collections import namedtuple
from typing import Literal, Union, Optional
from uuid import UUID

from generator.src.models.context import context, NewContent, NewPromo, NewReviewsLikes
from generator.src.models.notifications import Task, DeliveryType, EventType, Event
from generator.src.service.connector import AuthenticatedSession
from generator.src.service.communicators import AuthConnection, UGCConnection, ApiConnection, PGConnection
from generator.src.utils.auth import get_access_token



class ProcessTask:

    def __init__(self):
        self.connection = next(self._get_connect())

    @staticmethod
    def _get_connect(token=get_access_token()):
        """Establish connections with other app modules and close it at the end."""
        ugc_connection = UGCConnection(AuthenticatedSession(auth_token=token))
        auth_connection = AuthConnection(AuthenticatedSession(auth_token=token))
        api_connection = ApiConnection(AuthenticatedSession(auth_token=token))
        # TODO: deal with tokens
        pg_connection = PGConnection()

        Connection = namedtuple('Connection', ['ugc', 'auth', 'api', 'postgres'])
        yield Connection(ugc_connection, auth_connection, api_connection, pg_connection)

        ugc_connection.close()
        auth_connection.close()

    @staticmethod
    def _form_event(task: Task, content_type: Union[context], **kwargs) -> Event:
        """Form Event that should be sent."""
        # get list of keys in model's schema
        keys = list(content_type.__annotations__.keys())
        # get from kwargs only keys that match the schema's keys
        new_kwargs = {key: value for key, value in kwargs if key in keys}
        event = {
            "notification_id": UUID,
            "event_type": task.event_type,
            "delivery_type": task.delivery_type,
            "context": content_type(**new_kwargs)
        }
        return Event(**event)

    def _get_reviews_from_db(self) -> list[dict]:
        """Return reviews data from Notifications DB."""
        return self.connection.postgres.fetch_table(f"SELECT * FROM reviews_table;")

    def _filter_increased_likes(self) -> list[dict]:
        """Return all records from Notifications DB, when likes count in DB is less than current amount."""
        db_records = self._get_reviews_from_db()
        filtered_reviews = []
        for record in db_records:
            current_likes = self.connection.ugc.get_likes_count(record["review_id"])
            if current_likes > record["likes_count"]:
                filtered_reviews.append(record)
        return filtered_reviews

    def _send_new_content_events(self, task: Task) -> None:
        """Send NewContent or NewPromo events."""
        all_subscribed_users = self.connection.ugc.get_content_subscribers(task.context.movie_id)
        filtered_users = self.connection.auth.filter_users(all_subscribed_users, [{"TZ": True}])
        for user in filtered_users:
            event = self._form_event(task, NewContent, kwagrs=dict(task.context) | {"user_id": user})
            self.connection.api.send_event(event)

    def _send_updated_reviews(self, task: Task) -> None:
        """Send NewReviewsLikes events."""
        reviews = self._filter_increased_likes()
        for review in reviews:
            event = self._form_event(task, NewReviewsLikes, kwagrs=review)
            self.connection.api.send_event(event)

    def _send_promo_events(self, task: Task) -> None:
        """Send promo events."""
        group_users = self.connection.auth.get_user_group(task.context.group_id)
        filtered_users = self.connection.auth.filter_users(group_users, [{"TZ": True}])
        for user in filtered_users:
            event = self._form_event(task, NewPromo, kwagrs=dict(task.context) | {"user_id": user})
            self.connection.api.send_event(event)

    def _process_email_task(self, task: Task):
        """Handle email tasks."""
        if task.event_type == EventType.new_content:
            self._send_new_content_events(task)
        elif task.event_type == EventType.new_likes:
            self._send_updated_reviews(task)
        elif task.event_type == EventType.promo:
            self._send_promo_events(task)


    def perform_task(self, task: Task):
        """
        Single entry to start generating and sending notifications to Enricher.
        Receive task from scheduler and proceed.
        """
        if task.delivery_type == DeliveryType.email:
            self._process_email_task(task)
        elif task.delivery_type in [DeliveryType.push, DeliveryType.sms]:
            raise NotImplementedError("Delivery type not implemented yet")
