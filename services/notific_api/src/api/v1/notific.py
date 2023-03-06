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
    service: RabbitMQProducerService = Depends(get_producer_service),
    payload: dict = {'msg': 'test'},  # noqa: B006
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK
