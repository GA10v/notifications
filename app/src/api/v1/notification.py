import json

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.src.service.admin import AdminRequestInfo, AdminService, get_admin_service
from app.src.service.review import (
    ContentAnswerSchema,
    ReviewAnswerSchema,
    ReviewContentSchema,
    ReviewSaveSchema,
    ReviewService,
    get_review_service,
)
from app.src.service.user import UserWelcomeSchema, WelcomeUserService, get_welcome_service

router = APIRouter()


@router.post('/review', response_model=ReviewAnswerSchema)
async def save_review_notification(
    review_info: ReviewSaveSchema,
    review_service: ReviewService = Depends(get_review_service),
):
    review_answer = await review_service.save_review_notification(review_info)
    if review_answer.status:
        return JSONResponse(json.loads(review_answer.json()), status_code=200)
    return JSONResponse(json.loads(review_answer.json()), status_code=409)


@router.put('/review', response_model=ContentAnswerSchema)
async def add_review_content(
    review_content: ReviewContentSchema,
    review_service: ReviewService = Depends(get_review_service),
):
    content_answer = await review_service.add_review_content(review_content)
    if content_answer.status:
        return JSONResponse(json.loads(content_answer.json()), status_code=200)
    return JSONResponse(json.loads(content_answer.json()), status_code=201)


@router.post('/welcome')
async def welcome_user(
    user_info: UserWelcomeSchema,
    welcome_service: WelcomeUserService = Depends(get_welcome_service),
):
    await welcome_service.welcome_user(user_info)
    return user_info


@router.post('/new_episode')
async def send_new_episode(
    new_episode_info: AdminRequestInfo,
    admin_service: AdminService = Depends(get_admin_service),
):
    await admin_service.send_new_episode(new_episode_info)
    return JSONResponse({'msg': 'New episode sent'}, status_code=200)


@router.post('/group_message')
async def send_group_message(
    group_message_info: AdminRequestInfo,
    admin_service: AdminService = Depends(get_admin_service),
):
    await admin_service.send_group_message(group_message_info)
    return JSONResponse({'msg': 'Group message sent'}, status_code=200)
