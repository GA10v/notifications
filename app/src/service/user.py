import uuid
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.utils import BaseOrjsonModel
from db.base import get_notification_storage
from app.src.service.broker import get_broker_connection
from app.src.utils.broker import Broker
from app.src.core.config import settings
from app.src.utils.notification_storage import NotificationStorage
from aio_pika import connection


class UserWelcomeSchema(BaseOrjsonModel):
    user_id: uuid.UUID
    email: str
    login: str


class WelcomeUserService:

    def __init__(self, storage: NotificationStorage, broker: Broker):
        self.storage = storage
        self.broker = broker

    async def welcome_user(self, welcome_info: UserWelcomeSchema):
        await self.storage.registrate_welcome_notification(
            user_id=welcome_info.user_id,
        )
        welcome_info.user_id = str(welcome_info.user_id)
        await self.broker.send(welcome_info.dict(), settings.rabbit.QUEUE_WELLCOME.lower())


@lru_cache()
def get_welcome_service(
    session: AsyncSession = Depends(get_notification_storage),
    broker: connection = Depends(get_broker_connection)
) -> WelcomeUserService:
    storage = NotificationStorage(session)
    broker = Broker(broker)
    return WelcomeUserService(storage, broker)
