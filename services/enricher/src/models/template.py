from datetime import datetime

from pydantic import BaseModel

from models.base import DeliveryType


class TemplateFromDB(BaseModel):
    subject: str
    template_files: str
    text_msg: str


class ReviewsFromDB(BaseModel):
    pkid: str
    movie_id: str
    author_id: str
    review_id: str
    likes_count: int
    modified: datetime


class TemplateToSender(BaseModel):
    notification_id: str
    user_id: str | None
    subject: str
    email_body: str
    ws_body: str | None
    recipient: list[str]
    delivery_type: DeliveryType
