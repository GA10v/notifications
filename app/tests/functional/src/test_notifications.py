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
