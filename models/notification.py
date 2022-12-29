import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, DateTime
from db.base import Base
from models.content import ContentType


class Notification(Base):
    __tablename__ = 'notification'

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content_id = Column(UUID(as_uuid=True))
    content_type = Column(Enum(ContentType))
    last_update = Column(DateTime(), nullable=True)
    last_notification_send = Column(DateTime(), nullable=True)
