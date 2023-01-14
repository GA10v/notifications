import enum
import uuid

from sqlalchemy import Column, Enum, Index
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.src.tools import BaseOrjsonModel
from db.base import Base


class ContentType(enum.Enum):
    new_film = 'new_film'
    new_user = 'new_user'
    review_like = 'review_like'
    custom_mail = 'custom'


class Content(Base):
    __tablename__ = 'content'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # noqa: VNE003
    content_id = Column(UUID(as_uuid=True))
    content_type = Column(Enum(ContentType))
    content = Column(JSON())

    __table_args__ = (Index('idx_content', content_id, content_type, unique=True),)


class ReviewContent(BaseOrjsonModel):
    like_counter: int
    template_path: str
