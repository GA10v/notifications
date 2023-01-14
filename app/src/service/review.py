import uuid
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.tools import BaseOrjsonModel
from app.src.tools.notification_storage import NotificationStorage
from db.base import get_notification_storage
from models.content import ReviewContent


class ReviewSaveSchema(BaseOrjsonModel):
    content_id: uuid.UUID
    user_id: uuid.UUID


class ReviewContentSchema(BaseOrjsonModel):
    content_id: uuid.UUID


class ReviewAnswerSchema(BaseOrjsonModel):
    content_id: uuid.UUID
    status: bool


class ContentAnswerSchema(BaseOrjsonModel):
    content_id: uuid.UUID
    like_counter: int
    status: bool


class ReviewService:
    def __init__(self, storage: NotificationStorage):
        self.storage = storage

    async def save_review_notification(self, review_info: ReviewSaveSchema) -> ReviewAnswerSchema:
        try:
            await self.storage.registrate_review_notification(
                content_id=review_info.content_id,
                user_id=review_info.user_id,
            )
            return ReviewAnswerSchema(content_id=review_info.content_id, status=True)
        except IntegrityError:
            return ReviewAnswerSchema(content_id=review_info.content_id, status=False)

    async def add_review_content(self, review_info: ReviewContentSchema) -> ContentAnswerSchema:
        review_content = await self.storage.get_review_content(review_info.content_id)
        if review_content is None:
            await self.storage.save_review_content(
                review_info.content_id,
                ReviewContent(like_counter=1, template_path='str_test'),
            )
            return ContentAnswerSchema(content_id=review_info.content_id, like_counter=1, status=False)
        else:
            update_review_content = ReviewContent.parse_raw(review_content.content)
            update_review_content.like_counter += 1
            await self.storage.update_review_content(content_id=review_info.content_id, content=update_review_content)
            return ContentAnswerSchema(
                content_id=review_info.content_id,
                like_counter=update_review_content.like_counter,
                status=True,
            )


@lru_cache()
def get_review_service(
    session: AsyncSession = Depends(get_notification_storage),
) -> ReviewService:
    storage = NotificationStorage(session)
    return ReviewService(storage)
