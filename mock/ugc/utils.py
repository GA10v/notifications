from datetime import datetime
from random import randint
from uuid import uuid4

from faker import Faker

from models import ReviewInfo

fake = Faker()


def get_fake_review_info(
    movie_id: str | None = None,
    user_id: str | None = None,
    review_id: str | None = None,
) -> ReviewInfo:
    if not movie_id:
        movie_id = uuid4()
    if not user_id:
        user_id = uuid4()
    if not review_id:
        review_id = uuid4()

    return ReviewInfo(
        id=str(review_id),
        movie_id=str(movie_id),
        text='Fake review text ...',
        author_id=str(user_id),
        pub_date=datetime.now(),
        likes=randint(0, 50),
        dislikes=randint(0, 50),
        author_score=7.8,
    ).dict()


def get_fake_group() -> list[str]:
    return [str(uuid4()) for _ in range(20)]
