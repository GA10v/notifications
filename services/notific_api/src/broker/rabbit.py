import json
from abc import ABC, abstractmethod
from typing import Any

import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message
from aio_pika.channel.Channel import AbstractChannel
from aio_pika.connection.Connection import AbstractRobustConnection
from aio_pika.exchange.Exchange import AbstractExchange
from aio_pika.queue.Queue import AbstractQueue

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
        **kwargs: dict[Any, Any],
    ) -> None:
        ...

    @abstractmethod
    async def send_msg(self, msg: dict[Any, Any], **kwargs: dict[Any, Any]) -> None:
        ...


class RabbitMQProducer(ProducerProtocol):
    def __init__(self) -> None:
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractChannel | None = None
        self.incoming_queue: AbstractQueue | None = None
        self.retry_queue: AbstractQueue | None = None
        self.incoming_exchange: AbstractExchange | None = None
        self.retry_exchange: AbstractExchange | None = None

    async def init_producer(
        self,
        uri: str,
        incoming_queue: str,
        retry_queue: str,
        incoming_exchange: str,
        retry_exchange: str,
        **kwargs: dict[Any, Any],
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

    async def send_msg(self, msg: dict[Any, Any], **kwargs: dict[Any, Any]) -> None:
        message = Message(
            body=json.dumps(msg).encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT,
            headers={},
        )
        if self.incoming_queue and self.incoming_exchange:
            await self.incoming_exchange.publish(
                message=message,
                routing_key=self.incoming_queue.name,
            )


producer: RabbitMQProducer = RabbitMQProducer()


async def get_producer() -> RabbitMQProducer:
    return producer
