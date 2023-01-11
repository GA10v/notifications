from aio_pika.abc import AbstractRobustConnection
from sqlalchemy.util import asyncio
from typing import Callable


class RabbitService:
    def __init__(self, connection: AbstractRobustConnection):
        self.connection = connection

    async def consume(self, queue: str, callback: Callable):
        channel = await self.connection.channel()
        queue = await channel.declare_queue(queue, durable=True)
        await queue.consume(callback)
        try:
            await asyncio.Future()
        finally:
            await self.connection.close()
