import asyncio
import json
from abc import ABC, abstractmethod
from typing import Coroutine, Optional

from broker.rabbit import RabbitMQBroker
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class ConsumerProtocol(ABC):
    @abstractmethod
    async def consume(self, callback: Optional[Coroutine], **kwargs) -> None:
        ...


class RabbitMQConsumer(ConsumerProtocol, RabbitMQBroker):
    def __init__(
        self,
        incoming_queue: str = settings.rabbit.QUEUE_TO_ENRICH.lower(),
        retry_queue: str = settings.rabbit.QUEUE_RETRY_ENRICH.lower(),
        incoming_exchange: str = settings.rabbit.EXCHENGE_INCOMING_1.lower(),
        retry_exchange: str = settings.rabbit.EXCHENGE_RETRY_1.lower(),
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.incoming_queue = incoming_queue
        self.retry_queue = retry_queue
        self.incoming_exchange = incoming_exchange
        self.retry_exchange = retry_exchange

    async def consume(self, callback: Optional[Coroutine] = None, **kwargs) -> None:
        if not self.channel_pool:
            await self.get_channel_pool()

        async with self.channel_pool.acquire() as channel:
            await channel.set_qos(prefetch_count=10)
            incoming_queue = await channel.declare_queue(
                name=self.incoming_queue,
                durable=True,
                auto_delete=False,
                arguments={
                    'x-dead-letter-exchange': self.retry_exchange,
                    'x-message-ttl': 5000,
                },
            )
            retry_queue = await channel.declare_queue(
                name=self.retry_queue,
                durable=True,
                arguments={
                    'x-dead-letter-exchange': self.incoming_exchange,
                    'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
                },
            )
            await incoming_queue.bind(self.incoming_exchange)
            await retry_queue.bind(self.retry_exchange)
            async with incoming_queue.iterator() as queue_iter:
                async for message in queue_iter:
                    if callback is not None:
                        logger.info(f'Message from<{message.routing_key}> : body<{message.body}>')
                        await callback(json.loads(message.body))
                    # await message.reject()
                    await message.ack()
        await asyncio.Future()
