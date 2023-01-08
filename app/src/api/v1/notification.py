from fastapi import APIRouter, Depends

from app.src.service.review import ReviewSaveSchema, get_review_service, ReviewService, ReviewContentSchema
from app.src.service.user import UserWelcomeSchema, WelcomeUserService, get_welcome_service

router = APIRouter()


@router.post('/review')
async def save_review_notification(review_info: ReviewSaveSchema,
                                   review_service: ReviewService = Depends(get_review_service)):
    # TODO нужна проверка на уникальность (самое правильное решение - создать индекс)
    await review_service.save_review_notification(review_info)
    return review_info


@router.put('/review')
async def add_review_content(review_content: ReviewContentSchema,
                             review_service: ReviewService = Depends(get_review_service)):
    await review_service.add_review_content(review_content)
    return review_content


@router.post('/welcome')
async def welcome_user(user_info: UserWelcomeSchema,
                       welcome_service: WelcomeUserService = Depends(get_welcome_service)):
    await welcome_service.welcome_user(user_info)
    return user_info
