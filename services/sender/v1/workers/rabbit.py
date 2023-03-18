"""Collect data from rabbit pass it to worker."""

import asyncio
import json

import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool
from v1.workers.mail_worker import EmailWorker
from v1.workers.sms_worker import SMSWorker
from v1.workers.websocket_worker import WebSocketWorker

from core.config import settings
from core.logger import get_logger
from models.notifications import TemplateToSender

logger = get_logger(__name__)

WORKERS = {
    'email': EmailWorker,
    'websocket': WebSocketWorker,
    'sms': SMSWorker,
}


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbit.uri)


async def get_channel(connection_pool: Pool) -> aio_pika.Channel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()


async def consume(channel_pool: Pool) -> None:
    async with channel_pool.acquire() as channel:
        await channel.set_qos(prefetch_count=10)
        incoming_queue = await channel.declare_queue(
            name=settings.rabbit.QUEUE_TO_SEND.lower(),
            durable=True,
            auto_delete=False,
            arguments={
                'x-dead-letter-exchange': settings.rabbit.EXCHENGE_RETRY_2.lower(),
                'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
            },
        )
        retry_queue = await channel.declare_queue(
            name=settings.rabbit.QUEUE_RETRY_SEND.lower(),
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.rabbit.EXCHENGE_INCOMING_2.lower(),
                'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
            },
        )
        incoming_exchange = await channel.declare_exchange(
            name=settings.rabbit.EXCHENGE_INCOMING_2.lower(),
            type=ExchangeType.DIRECT,
            durable=True,
        )
        retry_exchange = await channel.declare_exchange(
            name=settings.rabbit.EXCHENGE_RETRY_2.lower(),
            type=ExchangeType.FANOUT,
            durable=True,
        )
        await incoming_queue.bind(incoming_exchange)
        await retry_queue.bind(retry_exchange)
        async with incoming_queue.iterator() as queue_iter:
            async for message in queue_iter:
                logger.info(f'Message from<{message.routing_key}> : body<{message.body}>')
                notification = TemplateToSender(**json.loads(message.body))
                await WORKERS[notification.delivery_type.value]().send_message(notification=notification)
                await message.ack()


async def main() -> None:
    loop = asyncio.get_event_loop()
    connection_pool: Pool = Pool(
        get_connection,
        max_size=settings.rabbit.CONNECT_POOL_SIZE,
        loop=loop,
    )
    channel_pool: Pool = Pool(
        get_channel,
        connection_pool,
        max_size=settings.rabbit.CONNECT_POOL_SIZE,
        loop=loop,
    )
    async with connection_pool, channel_pool:
        task = loop.create_task(consume(channel_pool))
        await task


if __name__ == '__main__':
    asyncio.run(main())
