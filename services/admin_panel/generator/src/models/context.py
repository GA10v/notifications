from pydantic import BaseModel


class NewReviewsLikes(BaseModel):
    # the same names as in DB
    review_id: str
    author_id: str
    movie_id: str
    likes_count: int

    movie_id - id фильма,
    author_id - id автора обзора,
    review_id - id обзора
    likes_count


class NewContent(BaseModel):
    user_id: str
    movie_id: str


class NewPromo(BaseModel):
    user_id: str
    text_to_promo: str
