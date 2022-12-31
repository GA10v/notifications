import uuid
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.utils import BaseOrjsonModel
from db.base import get_notification_storage
from models.content import ReviewContent
from utils.notification_storage import NotificationStorage


class ReviewSaveSchema(BaseOrjsonModel):
    content_id: uuid.UUID
    user_id: uuid.UUID


class ReviewContentSchema(BaseOrjsonModel):
    content_id: uuid.UUID


class ReviewService:

    def __init__(self, storage: NotificationStorage):
        self.storage = storage

    async def save_review_notification(self, review_info: ReviewSaveSchema):
        await self.storage.registrate_review_notification(
            content_id=review_info.content_id,
            user_id=review_info.user_id,
        )

    async def add_review_content(self, review_info: ReviewContentSchema):
        review_content = await self.storage.get_review_content(review_info.content_id)
        if review_content is None:
            await self.storage.save_review_content(review_info.content_id,
                                                   ReviewContent(like_counter=1, template_path='str_test'))
        else:
            review_content = ReviewContent.parse_raw(review_content.content)
            review_content.like_counter += 1
            await self.storage.update_review_content(content_id=review_info.content_id,
                                                     content=review_content)


@lru_cache()
def get_review_service(
    session: AsyncSession = Depends(get_notification_storage)
) -> ReviewService:
    storage = NotificationStorage(session)
    return ReviewService(storage)
