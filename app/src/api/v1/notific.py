from http import HTTPStatus

from core.config import settings
from fastapi import APIRouter
from service import producer

router = APIRouter()


@router.post(
    '/send_1',
    summary='Уведомления',
    description='Отправка уведомления в очередь RebbitMQ',
)
async def new_notific_1():
    await producer.send(
        msg={
            'notification_id': '6c162475-c7ed-4461-9184-001ef3d9f264',
            'template_id': '96dcc8f1-0b5e-4ed1-864f-264b9449acd2',
            'context': {
                'users_id': [
                    'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a',
                    '26e83050-29ef-4163-a99d-b546cac208f8',
                ],
                'payload': [
                    {
                        'film_id': '8f092fcd-1744-464f-a783-d9a6c4ec59d5',
                        'film_name': 'Film_1',
                        'link': 'http://localhost:15672/#/queues',
                    },
                ],
            },
        },
        queue=settings.rabbit.QUEUE_1.lower(),
    )
    return HTTPStatus.OK


@router.post(
    '/send_2',
    summary='Уведомления',
    description='Отправка уведомления в очередь RebbitMQ',
)
async def new_notific_2():
    await producer.send(
        msg={
            'notification_id': '6c162475-c7ed-4461-9184-001ef3d9f264',
            'template_id': '96dcc8f1-0b5e-4ed1-864f-264b9449acd2',
            'context': {'user_id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'link': 'http://localhost:15672/#/queues'},
        },
        queue=settings.rabbit.QUEUE_2.lower(),
    )
    return HTTPStatus.OK
