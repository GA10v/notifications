from typing import Union

from models.base import DeliveryType
from pydantic import BaseModel


class BaseUserContext(BaseModel):
    user_name: str
    email: str
    phone_number: str | None
    telegram_name: str | None
    delivery_type: DeliveryType


class NewUserContext(BaseModel):
    user_name: str
    email: str
    link: str
    delivery_type: DeliveryType


class NewReviewsLikesContext(BaseUserContext):
    movie_title: str
    likes: int


class NewContentContext(BaseUserContext):
    movie_title: str


class NewPromoContext(BaseModel):
    ...  # TODO узнать что отдавать на рендер


payload = Union[NewUserContext, NewReviewsLikesContext, NewContentContext, NewPromoContext]
