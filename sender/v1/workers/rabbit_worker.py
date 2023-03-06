"""Collect data from rabbit pass it to worker."""

import asyncio
import logging
from functools import partial
from typing import Callable

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from sender.settings.config import settings
from sender.v1.workers import mail_worker, websocket_worker

WORKERS = {
    'mail': mail_worker,
    'websocket': websocket_worker,
}


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbitmq_url)


async def get_channel(connection_pool: Pool) -> aio_pika.Channel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()


async def consume(channel_pool: Pool) -> None:
    async with channel_pool.acquire() as channel:
        await channel.set_qos(1)
        queue = await channel.queue_declare(
            settings.rabbitmq_sender_queue,
            auto_delete=False,
        )
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await WORKERS[message['method']].send_message(message)
                await message.ack()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    connection_pool: Pool = Pool(
        get_connection,
        max_size=settings.rabbitmq_pool_size,
        loop=loop,
    )
    get_channel_func: Callable = partial(
        get_channel(connection_pool=connection_pool),  # type: ignore[arg-type]
    )
    channel_pool: Pool = Pool(
        get_channel_func,
        max_size=settings.rabbitmq_channel_pool_size,
        loop=loop,
    )
    consumer: Callable = partial(consume(channel_pool=channel_pool))  # type: ignore[arg-type]
    async with connection_pool, channel_pool:
        task = loop.create_task(consumer())
        await task


if __name__ == '__main__':
    asyncio.run(main())
