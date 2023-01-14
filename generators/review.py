import asyncio
import datetime
import json
import uuid

from aio_pika import Message, connection
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.src.core.config import settings
from app.src.service.broker import get_broker_connection
from db.base import async_session
from models.content import Content, ContentType
from models.notification import Notification
from models.subscription import Subscription
from utils.users import UserInfoSchema, get_user_service


class NotificationSchema(BaseModel):
    notification_id: uuid.UUID
    content: dict
    user: UserInfoSchema
    last_update: datetime.datetime


class ReviewNotifications:
    notifications: list[NotificationSchema]

    def __init__(self, session: AsyncSession, broker: connection):
        self.session = session
        self.broker = broker

    async def get_notifications_info(self, last_update) -> None:
        c1 = aliased(Content)
        s1 = aliased(Subscription)
        s = (
            select(
                Notification.notification_id,
                Notification.content_id,
                Notification.content_type,
                Notification.last_update,
                c1.content,
                s1.user_id,
            )
            .select_from(
                Notification,
                c1,
                s1,
            )
            .where(
                Notification.last_update > datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S.%f'),
                Notification.content_type == ContentType.review_like,
            )
            .join(
                c1,
                Notification.content_id == c1.content_id,
            )
            .join(s1, Notification.notification_id == s1.notification_id)
        )

        result = await self.session.execute(s)
        user_service = get_user_service()
        notifications_info = result.mappings().all()
        users_id = [notification_info.get('user_id') for notification_info in notifications_info]
        users = {user.user_id: user for user in user_service.get_users_info(users_id)}

        notifications = []
        for notification in notifications_info:
            notifications.append(
                NotificationSchema(
                    notification_id=notification.get('notification_id'),
                    user=users.get(notification.get('user_id')),
                    content=json.loads(notification.get('content')),
                    last_update=notification.get('last_update'),
                ),
            )

        self.notifications = notifications

    async def send_to_broker(self):
        notifications = [notification.json() for notification in self.notifications]
        if len(notifications) != 0:
            channel = await self.broker.channel()
            await channel.default_exchange.publish(
                Message(json.dumps(notifications).encode('utf-8')),
                routing_key=settings.rabbit.QUEUE_REVIEW.lower(),
            )
            await self.broker.close()

    def get_last_update(self, last_update):
        last_updates = [notification.last_update for notification in self.notifications]
        if len(last_updates) == 0:
            return last_update
        return datetime.datetime.strftime(max(last_updates), '%Y-%m-%d %H:%M:%S.%f')


async def main():
    async with async_session() as session:
        with open('generator_status.json', 'r') as json_file:
            last_update = json.load(json_file)
        broker = await get_broker_connection()
        async with broker:
            review_notification = ReviewNotifications(session, broker)
            await review_notification.get_notifications_info(last_update.get('last_update'))
            await review_notification.send_to_broker()
            last_update = review_notification.get_last_update(last_update.get('last_update'))
        with open('generator_status.json', 'w') as json_file:
            json.dump({'last_update': last_update}, json_file)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
