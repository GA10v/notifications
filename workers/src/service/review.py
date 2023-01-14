import asyncio
import json
from pathlib import Path
from uuid import UUID

import aio_pika

from db.base import async_session
from generators.review import NotificationSchema
from workers.src.service.consumer import RabbitService
from workers.src.service.db_service import DBService
from workers.src.service.sender import SenderProtocol


class ReviewWorker:
    db_service: DBService

    def __init__(
        self,
        rabbit_service: RabbitService,
        sender_service: SenderProtocol,
        queue_name: str,
    ) -> None:
        self.rabbit = rabbit_service
        self.sender = sender_service
        self.queue = queue_name

    @staticmethod
    async def _prepare_data(data) -> dict:
        _data = NotificationSchema.parse_raw(data)
        return {
            'subject': 'review',
            'email': _data.user.email,
            'payload': {
                'user_name': _data.user.name,
                'like_count': _data.content.get('like_counter'),
            },
        }

    async def confirm_send_message(self, notification_id: UUID) -> None:
        async with async_session() as session:
            self.db_service = DBService(session)
            await self.db_service.confirm_review_send_message(notification_id)

    async def handling_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        template_path = Path(Path(__file__).parent.parent.parent.parent, 'templates')

        async with message.process():
            notifications = json.loads(message.body)
            send_tasks = []
            notifications_data = []
            for notification in notifications:
                send_data = await self._prepare_data(notification)
                notifications_data.append(NotificationSchema.parse_raw(notification).notification_id)
                send_tasks.append(self.sender.send(send_data, template_path, 'review.html'))
            statuses = await asyncio.gather(*send_tasks)

            confirm_tasks = []
            for i, status in enumerate(statuses):
                if status:
                    self.db_service = DBService(async_session())
                    confirm_tasks.append(self.confirm_send_message(notifications_data[i]))
            await asyncio.gather(*confirm_tasks)

    async def run(self) -> None:
        await self.sender.connect()
        await self.rabbit.consume(self.queue, self.handling_message)
        await self.sender.disconnect()
