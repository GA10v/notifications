import json
from abc import ABC, abstractmethod

from aio_pika import Message, connection


class AbsBroker(ABC):
    @abstractmethod
    async def send(self, msg: dict, queue: str) -> None:
        pass


class Broker(AbsBroker):
    def __init__(self, broker: connection):
        self.broker = broker

    async def send(self, msg: dict, queue: str) -> None:
        channel = await self.broker.channel()

        await channel.default_exchange.publish(Message(json.dumps(msg).encode('utf-8')), routing_key=queue)
        await self.broker.close()
