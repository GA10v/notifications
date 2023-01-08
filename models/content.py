import uuid
import enum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy import Column, Enum
from db.base import Base
from utils import BaseOrjsonModel


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


class ReviewContent(BaseOrjsonModel):
    like_counter: int
    template_path: str
