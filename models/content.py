import uuid
import enum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy import Column, Enum, Index
from db.base import Base
from app.src.utils import BaseOrjsonModel


class ContentType(enum.Enum):
    new_film = 'new_film'
    new_user = 'new_user'
    review_like = 'review_like'


class Content(Base):
    __tablename__ = 'content'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content_id = Column(UUID(as_uuid=True))
    content_type = Column(Enum(ContentType))
    content = Column(JSON())

    __table_args__ = (
        Index('idx_content', content_id, content_type, unique=True),
    )


class ReviewContent(BaseOrjsonModel):
    like_counter: int
    template_path: str
