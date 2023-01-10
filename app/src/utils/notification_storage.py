import datetime
from typing import Optional
from uuid import UUID
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.content import ContentType
from models.notification import Notification
from models.subscription import Subscription
from models.content import Content, ReviewContent


class AbsNotificationStorage(ABC):

    @abstractmethod
    async def registrate_review_notification(self, content_id: UUID, user_id: UUID) -> None:
        pass


class NotificationStorage(AbsNotificationStorage):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def registrate_review_notification(self, content_id: UUID, user_id: UUID) -> None:
        notification = Notification(content_id=content_id,
                                    content_type=ContentType.review_like,
                                    last_update=datetime.datetime.utcnow(),
                                    )
        self.session.add(notification)
        await self.session.commit()
        subscription = Subscription(user_id=user_id, notification_id=notification.notification_id)
        self.session.add(subscription)
        await self.session.commit()

    async def get_review_content(self, content_id: UUID) -> Optional[Content]:
        result = await self.session.execute(
            select(Content).where(
                Content.content_id == content_id, Content.content_type == ContentType.review_like))

        scalar_result = result.scalars().all()
        if len(scalar_result) == 0:
            return None
        return scalar_result[0]

    async def save_review_content(self, content_id: UUID, content: ReviewContent) -> None:
        content = Content(content_id=content_id, content_type=ContentType.review_like, content=content.json())
        self.session.add(content)
        await self.session.commit()

    async def update_review_content(self, content_id: UUID, content: ReviewContent) -> None:
        content_from_db = await self.get_review_content(content_id=content_id)
        content_from_db.content = content.json()
        self.session.add(content_from_db)
        await self.session.commit()

    async def registrate_welcome_notification(self, user_id: UUID):
        notification = Notification(content_id=user_id, content_type=ContentType.new_user)
        self.session.add(notification)
        await self.session.commit()
        subscription = Subscription(user_id=user_id, notification_id=notification.notification_id)
        self.session.add(subscription)
        await self.session.commit()
