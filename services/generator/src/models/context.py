from pydantic import BaseModel


class NewReviewsLikes(BaseModel):
    # the same names as in DB
    review_id: str
    author_id: str
    movie_id: str
    likes_count: int


class NewContent(BaseModel):
    user_id: str
    movie_id: str


class NewPromo(BaseModel):
    user_group_id: str


context = [NewContent, NewReviewsLikes, NewPromo]
