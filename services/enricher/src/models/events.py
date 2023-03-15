from datetime import datetime

from pydantic import BaseModel

from models.base import DeliveryType, EventType
from models.context import context


class Event(BaseModel):
    notification_id: str
    source_name: str
    event_type: EventType
    delivery_type: DeliveryType
    context: context
    created_at: datetime
