import json
import uuid
from functools import lru_cache

from aio_pika import connection, Message
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.config import settings
from app.src.service.broker import get_broker_connection
from app.src.tools import BaseOrjsonModel

from db.base import get_notification_storage
from models.content import ContentType
from models.subscription import Subscription
from models.notification import Notification
from utils.users import get_user_service, UserInfoProtocol, UserInfoSchema


class AdminRequestInfo(BaseOrjsonModel):
    content_id: uuid.UUID
    content: dict


class AdminBrokerInfo(BaseOrjsonModel):
    user: UserInfoSchema
    content_id: uuid.UUID
    content: dict


class AdminService:

    def __init__(self, session: AsyncSession, broker: connection, user_service: UserInfoProtocol):
        self.session = session
        self.broker = broker
        self.user_service = user_service

    async def get_new_episode_notifications(self, content_id: uuid.UUID, content: dict) -> list[AdminBrokerInfo]:
        query = select(Subscription.user_id).where(
            Subscription.notification_id.in_(select(
                Notification.notification_id).where(
                Notification.content_id == content_id, Notification.content_type == ContentType.new_film)))
        result = await self.session.execute(query)
        user_ids = [str(user_id) for (user_id,) in result.all()]

        if not user_ids:
            return []
        users = self.user_service.get_users_info(user_ids)

        return [AdminBrokerInfo(user=user, content=content, content_id=content_id) for user in users]

    async def get_group_message_notifications(self, content: dict) -> list[AdminBrokerInfo]:
        user_role = content.get('user_role')

        if not user_role:
            return []

        users = self.user_service.get_users_info_by_role(user_role)
        return [AdminBrokerInfo(user=user, content=content) for user in users]

    async def send_to_broker(self, msg: list[str], queue: str) -> None:
        channel = await self.broker.channel()

        await channel.default_exchange.publish(
            Message(
                json.dumps(msg).encode('utf-8')
            ),
            routing_key=queue
        )
        await self.broker.close()

    async def send_new_episode(self, admin_info: AdminRequestInfo) -> None:
        content_id = admin_info.content_id
        content = admin_info.content
        notifications = await self.get_new_episode_notifications(content_id, content)

        if notifications:
            msg = [notification.json() for notification in notifications]
            await self.send_to_broker(msg, settings.rabbit.QUEUE_EPISODE.lower())

    async def send_group_message(self, admin_info: AdminRequestInfo) -> None:
        content = admin_info.content
        notifications = await self.get_group_message_notifications(content)

        if notifications:
            msg = [notification.json() for notification in notifications]
            await self.send_to_broker(msg, settings.rabbit.QUEUE_MESSAGE.lower())


@lru_cache()
def get_admin_service(
    session: AsyncSession = Depends(get_notification_storage),
    broker: connection = Depends(get_broker_connection),
    user_sevice: UserInfoProtocol = Depends(get_user_service)
) -> AdminService:
    return AdminService(session, broker, user_sevice)
