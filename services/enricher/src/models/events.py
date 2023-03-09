from datetime import datetime

from models.base import DeliveryType, EventType
from models.context import context
from pydantic import BaseModel


class Event(BaseModel):
    source_name: str
    event_type: EventType
    delivery_type: DeliveryType
    context: context
    created_at: datetime
