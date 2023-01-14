import enum
import uuid

from sqlalchemy import Boolean, Column, Enum
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base


class CommunicationType(enum.Enum):
    ws = 'ws'
    email = 'email'
    telegram = 'telegram'


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # noqa: VNE003
    user_id = Column(UUID(as_uuid=True))
    communication_method = Column(Enum(CommunicationType))
    allow_communication = Column(Boolean())
