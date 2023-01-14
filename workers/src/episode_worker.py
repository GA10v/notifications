import asyncio

import aio_pika

from workers.src.core.config import settings
from workers.src.service.consumer import RabbitService
from workers.src.service.episode import EpisodeWorker
from workers.src.service.sender import EmailSender


async def main() -> None:
    rabbit_connection = await aio_pika.connect_robust(settings.rabbit.uri)
    rabbit_service = RabbitService(rabbit_connection)
    sender_service = EmailSender(
        host=settings.smtp.HOST,
        port=settings.smtp.PORT,
        user=settings.smtp.USER,
        password=settings.smtp.PASSWODR,
    )
    queue = settings.rabbit.QUEUE_EPISODE

    worker = EpisodeWorker(rabbit_service=rabbit_service, sender_service=sender_service, queue_name=queue.lower())
    await worker.run()


if __name__ == '__main__':
    asyncio.run(main())
