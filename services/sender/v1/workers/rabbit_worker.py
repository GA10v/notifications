"""Collect data from rabbit pass it to worker."""

import asyncio
import json
import logging
from typing import Any

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool
from v1.workers import mail_worker, sms_worker, websocket_worker

from core.config import settings
from models.notifications import TemplateToSender

WORKERS = {
    'mail': mail_worker,
    'websocket': websocket_worker,
    'sms': sms_worker,
}


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbit.uri)


async def get_channel(connection_pool: Pool[Any]) -> Any:
    async with connection_pool.acquire() as connection:
        return await connection.channel()


async def consume(channel_pool: Pool[Any]) -> None:
    async with channel_pool.acquire() as channel:
        await channel.set_qos(1)
        queue = await channel.declare_queue(
            settings.rabbit.QUEUE_TO_SEND,
            auto_delete=False,
        )
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                notification = TemplateToSender(json.loads(message))
                await WORKERS[message['method']].send_message(notification)
                await message.ack()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    connection_pool: Pool[Any] = Pool(
        get_connection,
        max_size=settings.rabbit.CONNECT_POOL_SIZE,
        loop=loop,
    )
    channel_pool: Pool[Any] = Pool(
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
