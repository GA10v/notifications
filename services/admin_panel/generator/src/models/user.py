from datetime import date, datetime

from pydantic import BaseModel

from generator.src.models.notifications import DeliveryType


class User(BaseModel):
    user_id: str  # TODO: or UUID?
    first_name: str
    last_name: str
    email: str | None
    phone_number: str | None
    telegram_name: str | None
    gender: str | None
    country: str | None
    time_zone: datetime | None
    birthday: date | None
    delivery_type: list[DeliveryType]
    accept_promo: bool
