import json
from abc import ABC, abstractmethod

import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message
from core.config import settings


class ProducerProtocol(ABC):
    @abstractmethod
    async def init_producer(
        self,
        uri: str,
        incoming_queue: str,
        retry_queue: str,
        incoming_exchange: str,
        retry_exchange: str,
        **kwargs,
    ) -> None:
        ...

    @abstractmethod
    async def send_msg(self, msg: dict, **kwargs) -> None:
        ...


class RabbitMQProducer(ProducerProtocol):
    def __init__(self) -> None:
        self.connection = None
        self.channel = None
        self.incoming_queue = None
        self.retry_queue = None
        self.incoming_exchange = None
        self.retry_exchange = None

    async def init_producer(
        self,
        uri: str,
        incoming_queue: str,
        retry_queue: str,
        incoming_exchange: str,
        retry_exchange: str,
        **kwargs,
    ) -> None:
        self.connection = await aio_pika.connect_robust(uri)
        self.channel = await self.connection.channel()
        self.incoming_queue = await self.channel.declare_queue(
            name=incoming_queue,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.rabbit.EXCHENGE_RETRY_1.lower(),
                'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
            },
        )
        self.retry_queue = await self.channel.declare_queue(
            name=retry_queue,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.rabbit.EXCHENGE_INCOMING_1.lower(),
                'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
            },
        )
        self.incoming_exchange = await self.channel.declare_exchange(
            name=incoming_exchange,
            type=ExchangeType.DIRECT,
            durable=True,
        )
        self.retry_exchange = await self.channel.declare_exchange(
            name=retry_exchange,
            type=ExchangeType.FANOUT,
            durable=True,
        )

        await self.incoming_queue.bind(self.incoming_exchange)
        await self.retry_queue.bind(self.retry_exchange)

    async def send_msg(self, msg: dict, **kwargs) -> None:
        message = Message(
            body=json.dumps(msg).encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT,
            headers={},
        )
        await self.incoming_exchange.publish(
            message=message,
            routing_key=self.incoming_queue.name,
        )


producer: RabbitMQProducer = RabbitMQProducer()


async def get_producer() -> RabbitMQProducer:
    return producer
