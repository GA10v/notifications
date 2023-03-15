from pydantic import BaseModel

from models.base import DeliveryType


class TemplateFromDB(BaseModel):
    subject: str
    template_files: str
    text_msg: str


class TemplateToSender(BaseModel):
    notification_id: str
    user_id: str | None
    subject: str
    email_body: str
    ws_body: str | None
    recipient: list[str]
    delivery_type: DeliveryType
