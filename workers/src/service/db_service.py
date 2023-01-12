import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.content import ContentType
from models.notification import Notification


class DBService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def confirm_welcome_send_message(self, user_id: UUID):
        result = await self.session.execute(select(Notification).where(
                Notification.content_id == user_id, Notification.content_type == ContentType.new_user)
        )
        notification = result.scalars().all()[0]
        notification.last_notification_send = datetime.datetime.utcnow()
        self.session.add(notification)
        await self.session.commit()
