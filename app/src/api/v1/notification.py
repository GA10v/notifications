import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.src.service.review import (ReviewSaveSchema, get_review_service, ReviewService,
                                    ReviewContentSchema, ReviewAnswerSchema, ContentAnswerSchema)
from app.src.service.user import UserWelcomeSchema, WelcomeUserService, get_welcome_service
from app.src.utils import BaseOrjsonModel

router = APIRouter()


@router.post('/review', response_model=ReviewAnswerSchema)
async def save_review_notification(review_info: ReviewSaveSchema,
                                   review_service: ReviewService = Depends(get_review_service)):
    review_answer = await review_service.save_review_notification(review_info)
    if review_answer.status:
        return JSONResponse(review_answer.json(), status_code=200)
    return JSONResponse(review_answer.json(), status_code=409)


@router.put('/review', response_model=ContentAnswerSchema)
async def add_review_content(review_content: ReviewContentSchema,
                             review_service: ReviewService = Depends(get_review_service)):
    review_content = await review_service.add_review_content(review_content)
    if review_content.status:
        return JSONResponse(review_content.json(), status_code=200)
    return JSONResponse(review_content.json(), status_code=201)


@router.post('/welcome')
async def welcome_user(user_info: UserWelcomeSchema,
                       welcome_service: WelcomeUserService = Depends(get_welcome_service)):
    await welcome_service.welcome_user(user_info)
    return user_info


class NewEpisodeInfo(BaseOrjsonModel):
    notification_id: uuid.UUID
    content: dict


@router.post('/new_episode')
async def send_new_episode(new_episode_info: NewEpisodeInfo):
    # Имея notification_id - найду всех юзеров подписанных на событие и отправлю им content
    ...


class GroupMessageInfo(BaseOrjsonModel):
    notification_id: uuid.UUID
    content: dict
    user_role: str
    template_path: str


@router.post('/group_message')
async def send_group_message(group_message_info: GroupMessageInfo):
    # Имея user_role - запрошу всех пользователей с этой ролью и отправлю content
    ...