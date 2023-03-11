from datetime import datetime
from enum import Enum
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


class EventType(str, Enum):
    welcome = 'welcome_message'
    new_content = 'new_content'
    new_likes = 'new_likes'
    promo = 'promo'

    def __repr__(self) -> str:
        return f'{self.value}'


class DeliveryType(str, Enum):
    email = "email"
    sms = "sms"
    push = "push"


class Notification(BaseModel):
    notification_id: UUID
    event_type: EventType
    delivery_type: list[DeliveryType]
    header: str
    template_path: str
    template_payload: Optional[list[str]]
    created_at: datetime
    updated_at: datetime


class NotificationLastSent(BaseModel):
    notification_id: UUID
    content_id: UUID
    payload: Any
    created_at: datetime
    updated_at: datetime
