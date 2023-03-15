from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from admin_panel.generator.src.models.context import NewContent, NewPromo, NewReviewsLikes


class EventType(str, Enum):
    new_content = 'new_content'
    new_likes = 'new_likes'
    promo = 'promo'

    def __repr__(self) -> str:
        return f'{self.value}'


class DeliveryType(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'

class Task(BaseModel):
    event_type: EventType
    movie_id: str | None
    group_id: str | None
    text_to_promo: str | None


class Event(BaseModel):
    notification_id: UUID
    event_type: EventType
    context: NewContent | NewReviewsLikes | NewPromo
    created_at: datetime
    source_name: str
