from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from service.producer import RabbitMQProducerService, get_producer_service

router = APIRouter()


@router.post(
    '/send',
    summary='Notification',
    description='Отправка уведомления в очередь RebbitMQ',
)
async def send_notific(
    request: Request,
    payload: dict,  # noqa: B006
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_new_content',
    summary='Notification',
    description='Отправка уведомления в очередь RebbitMQ',
)
async def test_1(
    request: Request,
    payload: dict = {  # noqa: B006
        'notific_id': 'fake_uuid',
        'source_name': 'Generator',
        'event_type': 'new_content',
        'delivery_type': 'email',
        'context': {
            'user_id': '122345',
            'movie_id': '654',
        },
        'created_at': '2023-03-07 20:29:40',
    },
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_likes',
    summary='Notification',
    description='Отправка уведомления в очередь RebbitMQ',
)
async def test_2(
    request: Request,
    payload: dict = {  # noqa: B006
        'notific_id': 'fake_uuid',
        'source_name': 'Generator',
        'event_type': 'new_likes',
        'delivery_type': 'email',
        'context': {
            'review_id': '5232',
            'author_id': '122345',
            'movie_id': '654',
            'likes': 20,
        },
        'created_at': '2023-03-07 20:29:40',
    },  # noqa: B006
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_welcome',
    summary='Notification',
    description='Отправка уведомления в очередь RebbitMQ',
)
async def test_3(
    request: Request,
    payload: dict = {  # noqa: B006
        'notific_id': 'fake_uuid',
        'source_name': 'Auth',
        'event_type': 'welcome_message',
        'delivery_type': 'email',
        'context': {
            'user_id': '5232',
            'name': 'Fake User',
            'email': 'fake@fake.com',
        },
        'created_at': '2023-03-07 20:29:40',
    },  # noqa: B006
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_promo',
    summary='Notification',
    description='Отправка уведомления в очередь RebbitMQ',
)
async def test_4(
    request: Request,
    payload: dict = {  # noqa: B006
        'notific_id': 'fake_uuid',
        'source_name': 'Generator',
        'event_type': 'promo',
        'delivery_type': 'email',
        'context': {
            'user_id': '5232',
            'text_to_promo': 'Bla Bla Bla',
        },
        'created_at': '2023-03-07 20:29:40',
    },  # noqa: B006
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK
