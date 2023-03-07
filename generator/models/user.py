from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel

from generator.models.notifications import DeliveryType


class User(BaseModel):
    id: UUID
    name: str
    last_name: str
    email: str | None
    phone_number: str | None
    telegram_name: str | None
    gender: str | None
    country: str | None
    time_zone: datetime | None
    birthday: date | None
    delivery_type: DeliveryType
