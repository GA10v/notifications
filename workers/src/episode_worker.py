import asyncio

import aio_pika
from workers.src.core.config import settings
from workers.src.service.consumer import RabbitService
from workers.src.service.sender import EmailSender
from workers.src.service.episode import EpisodeWorker


async def main():
    rabbit_connection = await aio_pika.connect_robust('amqp://guest:guest@172.24.0.3:5672')
    rabbit_service = RabbitService(rabbit_connection)
    sender_service = EmailSender()
    queue = settings.rabbit.QUEUE_EPISODE

    worker = EpisodeWorker(rabbit_service=rabbit_service,
                           sender_service=sender_service,
                           queue_name=queue.lower())
    await worker.run()


if __name__ == '__main__':
    asyncio.run(main())
