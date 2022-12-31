from fastapi import APIRouter, Depends

from service.review import ReviewSaveSchema, get_review_service, ReviewService, ReviewContentSchema

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
