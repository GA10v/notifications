import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, ForeignKey
from db.base import Base


class Subscription(Base):
    __tablename__ = 'subscription'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True))
    notification_id = Column(UUID(as_uuid=True), ForeignKey('notification.notification_id', ondelete='CASCADE'))
    last_notification_send_to_user = Column(DateTime(), nullable=True)
