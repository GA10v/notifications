from typing import Callable

from aio_pika.abc import AbstractRobustConnection
from sqlalchemy.util import asyncio


class RabbitService:
    def __init__(self, connection: AbstractRobustConnection):
        self.connection = connection

    async def consume(self, queue: str, callback: Callable):
        channel = await self.connection.channel()
        declare_queue = await channel.declare_queue(queue, durable=True)
        await declare_queue.consume(callback)
        try:
            await asyncio.Future()
        finally:
            await self.connection.close()
