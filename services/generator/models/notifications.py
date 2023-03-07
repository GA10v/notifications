from datetime import datetime
from enum import Enum
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


class EventType(str, Enum):
    welcome = "welcome_message"
    new_series = "new_series"
    birthday = "birthday_greetings"
    recommendations = "recommendations"
    promo = "promo"


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
