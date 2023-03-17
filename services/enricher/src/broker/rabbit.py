import asyncio
from abc import ABC, abstractmethod
from typing import Any

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractConnection
from aio_pika.pool import Pool

from core.config import settings


class BrokerProtocol(ABC):
    @abstractmethod
    async def get_connection(self, **kwargs: dict[Any, Any]) -> AbstractConnection:
        ...

    @abstractmethod
    async def get_channel(self, **kwargs: dict[Any, Any]) -> AbstractChannel:
        ...


class RabbitMQBroker(BrokerProtocol):
    def __init__(self, uri: str = settings.rabbit.uri, **kwargs: dict[Any, Any]) -> None:
        self.uri = uri
        self.channel_pool: Pool[Any] | None = None

    async def get_channel(self, **kwargs: dict[Any, Any]) -> AbstractChannel | Any:
        connection_pool = await self.get_connection_pool()
        async with connection_pool.acquire() as conn:
            return await conn.channel()

    async def get_connection(self, **kwargs: dict[Any, Any]) -> AbstractConnection:
        return await aio_pika.connect_robust(self.uri)

    async def get_channel_pool(self, **kwargs: dict[Any, Any]) -> None:
        loop = asyncio.get_event_loop()
        self.channel_pool = Pool(self.get_channel, max_size=10, loop=loop)

    async def get_connection_pool(self, **kwargs: dict[Any, Any]) -> Pool[Any]:
        loop = asyncio.get_event_loop()
        return Pool(self.get_connection, max_size=10, loop=loop)
