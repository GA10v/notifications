import asyncio
from typing import Any

from broker.consumer import RabbitMQConsumer
from broker.producer import RabbitMQProducer
from db.storage import PGStorage
from models.events import Event
from service.builder import BuilderService
from service.enrich.handler import get_payload
from service.template import get_template

consumer = RabbitMQConsumer()
producer = RabbitMQProducer()
enricher = BuilderService()
db = PGStorage()


async def handler(message: dict[str, Any]) -> None:
    event = Event(**message)
    async with db as conn:
        _template = await get_template(db=conn, data=event)
    payload = await get_payload(data=event)
    new_message = await enricher.build(data=payload, template=_template)
    print('handler new_message: ', new_message)  # noqa: T201
    await producer.publish(msg=new_message)


async def builder() -> None:
    await consumer.consume(callback=handler)


if __name__ == '__main__':
    asyncio.run(builder())
