import asyncio

import aio_pika
from core.config import settings
from service.consumer import RabbitService
from service.sender import EmailSender
from service.worker import Worker


async def main():
    rabbit_connection = await aio_pika.connect_robust(settings.rabbit.uri)
    rabbit_service = RabbitService(rabbit_connection)
    sender_service = EmailSender()
    queues = settings.rabbit.QUEUES

    workers = []
    for queue in queues:
        worker = Worker(rabbit_service=rabbit_service, sender_service=sender_service, queue_name=queue.lower())
        workers.append(worker.work())
    await asyncio.gather(*workers)
    await rabbit_connection.close()


if __name__ == '__main__':
    print('run')  # noqa: T201
    asyncio.run(main())
