from http import HTTPStatus

import pytest
from config import settings

pytestmark = pytest.mark.asyncio


async def test_review(session):
    """Проверка уведомлений по лайкам рецензии"""
    url = f'{settings.fastapi.service_url}/{settings.fastapi.REVIEW_ENDPOINT}'

    data = {
        'content_id': settings.data.CONTENT,
        'user_id': settings.data.USER
    }
    async with session.post(url, json=data) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body['content_id'] == settings.data.CONTENT

    async with session.post(url, json=data) as response:
        assert response.status == HTTPStatus.CONFLICT

    data = {
        'content_id': settings.data.CONTENT
    }

    async with session.put(url, json=data) as response:
        assert response.status == HTTPStatus.CREATED
        response_data = await response.json()
        assert response_data['content_id'] == settings.data.CONTENT
        assert response_data['like_counter'] == 1

    async with session.put(url, json=data) as response:
        assert response.status == HTTPStatus.OK
        response_data = await response.json()
        assert response_data['content_id'] == settings.data.CONTENT
        assert response_data['like_counter'] == 2


async def test_welcome(session):
    """Проверка уведомлений при регистрации пользователя"""
    url = f'{settings.fastapi.service_url}/{settings.fastapi.WELCOME_ENDPOINT}'

    data = {
        'user_id': settings.data.USER,
        'email': settings.data.EMAIL,
        'login': settings.data.LOGIN
    }
    async with session.post(url, json=data) as response:
        assert response.status == HTTPStatus.OK


async def test_new_episode(session):
    """Проверка уведомлений при добавлении нового фильма или новой серии"""
    url = f'{settings.fastapi.service_url}/{settings.fastapi.NEW_EPISODE_ENDPOINT}'

    data = {
        'notification_id': settings.data.NOTIFICATION_1,
        'content': {
            'art': settings.data.ART,
            'event': settings.data.EVENT
        }
    }
    async with session.post(url, json=data) as response:
        assert response.status == HTTPStatus.OK


async def test_group_message(session):
    """Проверка уведомлений при групповой рассылке"""
    url = f'{settings.fastapi.service_url}/api/v1/notification/group_message'

    data = {
        'notification_id': settings.data.NOTIFICATION_2,
        'content': {
            'user_role': settings.data.USER_ROLE,
            'template_path': settings.data.TEMPLATE_PATH
        }
    }
    async with session.post(url, json=data) as response:
        assert response.status == HTTPStatus.OK
