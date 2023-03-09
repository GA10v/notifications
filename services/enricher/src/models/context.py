from typing import Union

from pydantic import BaseModel


class NewUser(BaseModel):
    user_id: str
    name: str
    email: str


class NewReviewsLikes(BaseModel):
    author_id: str
    movie_id: str
    likes: int


class NewContent(BaseModel):
    user_id: str
    movie_id: str


class NewPromo(BaseModel):  # TODO узнать что будет приходить от админки
    ...


context = Union[NewUser, NewReviewsLikes, NewContent, NewPromo]
