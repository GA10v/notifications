import uuid

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from models.content import ContentType
from models.notification import Notification
from fastapi import APIRouter, Depends

from db.base import get_session


router = APIRouter()


class ReviewSaveSchema(BaseModel):
    content_id: uuid.UUID
    user_id: uuid.UUID


@router.post('/review')
async def save_review_notification(review: ReviewSaveSchema,
                                   session: AsyncSession = Depends(get_session)):
    notific = Notification(content_id=uuid.uuid4(), content_type=ContentType.new_user)
    session.add(notific)
    await session.commit()
    return review

