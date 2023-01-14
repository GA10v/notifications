import uuid
from functools import lru_cache

from aio_pika.abc import AbstractRobustConnection
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.core.config import settings
from app.src.service.broker import get_broker_connection
from app.src.tools import BaseOrjsonModel
from app.src.tools.broker import Broker
from app.src.tools.notification_storage import NotificationStorage
from db.base import get_notification_storage


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
        welcome_info.user_id = str(welcome_info.user_id)  # type: ignore
        await self.broker.send(welcome_info.dict(), settings.rabbit.QUEUE_WELLCOME.lower())


@lru_cache()
def get_welcome_service(
    session: AsyncSession = Depends(get_notification_storage),
    broker_connection: AbstractRobustConnection = Depends(get_broker_connection),
) -> WelcomeUserService:
    storage = NotificationStorage(session)
    broker = Broker(broker_connection)
    return WelcomeUserService(storage, broker)
