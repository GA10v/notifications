from models.base import DeliveryType
from pydantic import BaseModel


class TemplateFromDB(BaseModel):
    subject: str
    template_files: str
    text_msg: str
    text_to_promo: str | None


class TemplateToSender(BaseModel):
    user_id: str | None
    subject: str
    email_body: str
    ws_body: str | None
    recipient: list[str]
    delivery_type: DeliveryType
