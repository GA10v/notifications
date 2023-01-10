import json

from aio_pika.abc import AbstractRobustConnection


class RabbitService:
    def __init__(self, connection: AbstractRobustConnection):
        self.connection = connection

    async def consume(self, queue: str):
        async with self.connection.channel() as channel:
            queue = await channel.declare_queue(
                name=queue,
                durable=True,
            )
            async with queue.iterator() as iterator:
                async for data in iterator:
                    async with data.process():
                        return json.loads(data.body)
