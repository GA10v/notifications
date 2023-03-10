from uuid import UUID

from pydantic import BaseModel


class NotificationToDelivery(BaseModel):
    id: UUID
    subject: str
    message_body: str
    recepient: str
