import asyncio

import aio_pika

from db.base import async_session
from workers.src.core.config import settings
from workers.src.service.consumer import RabbitService
from workers.src.service.db_service import DBService
from workers.src.service.sender import EmailSender
from workers.src.service.welcome import WelcomeWorker


async def main():
    rabbit_connection = await aio_pika.connect_robust(settings.rabbit.uri)
    rabbit_service = RabbitService(rabbit_connection)
    sender_service = EmailSender(
        host=settings.smtp.HOST,
        port=settings.smtp.PORT,
        user=settings.smtp.USER,
        password=settings.smtp.PASSWODR,
    )
    queue = settings.rabbit.QUEUE_WELLCOME
    async with async_session() as session:
        worker = WelcomeWorker(rabbit_service=rabbit_service,
                               sender_service=sender_service,
                               queue_name=queue.lower(),
                               db_service=DBService(session))
        await worker.run()


if __name__ == '__main__':
    asyncio.run(main())
