import asyncio
from typing import Any

from broker.consumer import RabbitMQConsumer
from broker.producer import RabbitMQProducer
from service.builder import BuilderService

consumer = RabbitMQConsumer()
producer = RabbitMQProducer()
enricher = BuilderService()


async def handler(message: dict[str, Any]) -> None:
    print('handler message: ', message)  # noqa: T201
    new_message = await enricher.build(message)
    print('handler new_message: ', new_message)  # noqa: T201
    await producer.publish(msg=new_message)


async def builder() -> None:
    await consumer.consume(callback=handler)


if __name__ == '__main__':
    asyncio.run(builder())
