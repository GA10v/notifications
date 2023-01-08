import aio_pika
from aio_pika import ExchangeType, connection
from app.src.core.config import settings


async def get_broker_connection() -> connection:
    return await aio_pika.connect_robust(settings.rabbit.uri)


async def init_queue() -> None:
    connection = await get_broker_connection()
    channel = await connection.channel()
    # declare exchanges
    notific_exchange_1 = await channel.declare_exchange(
        settings.rabbit.EXCHENGE_1.lower(),
        ExchangeType.DIRECT,
        durable=True,
    )
    notific_exchange_2 = await channel.declare_exchange(
        settings.rabbit.EXCHENGE_2.lower(),
        ExchangeType.DIRECT,
        durable=True,
    )
    # declare queues
    notific_queue_1 = await channel.declare_queue(
        settings.rabbit.QUEUE_1.lower(),
        durable=True,
    )
    notific_queue_2 = await channel.declare_queue(
        settings.rabbit.QUEUE_2.lower(),
        durable=True,
    )
    # bind queues
    await notific_queue_1.bind(notific_exchange_1)
    await notific_queue_2.bind(notific_exchange_2)
