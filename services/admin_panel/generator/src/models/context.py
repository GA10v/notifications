from uuid import UUID

from pydantic import BaseModel


class NewReviewsLikes(BaseModel):
    # the same names as in DB
    review_id: UUID
    author_id: UUID
    movie_id: UUID
    likes_count: int


class NewContent(BaseModel):
    user_id: UUID
    movie_id: UUID


class NewPromo(BaseModel):
    user_id: UUID
    text_to_promo: str
