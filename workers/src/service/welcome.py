import json

import aio_pika
from pathlib import Path

from app.src.service.user import UserWelcomeSchema
from workers.src.service.consumer import RabbitService
from workers.src.service.db_service import DBService
from workers.src.service.sender import SenderProtocol


class WelcomeWorker:
    def __init__(
        self,
        db_service: DBService,
        rabbit_service: RabbitService,
        sender_service: SenderProtocol,
        queue_name: str,
    ) -> None:
        self.rabbit = rabbit_service
        self.db_service = db_service
        self.sender = sender_service
        self.queue = queue_name

    @staticmethod
    async def _prepare_data(data):
        _data = UserWelcomeSchema(**data)
        data = {
            'subject': 'registration',
            'email': _data.email,
            'payload': {
                'user_name': _data.login,
            },
        }
        return data

    async def handling_message(self, message: aio_pika.abc.AbstractIncomingMessage,):
        async with message.process():
            data = json.loads(message.body)
            send_data = await self._prepare_data(data)
            template_path = Path(Path(__file__).parent.parent.parent.parent, 'templates')
            is_send = await self.sender.send(send_data, template_path, 'new_user.html')
        if is_send:
            await self.db_service.confirm_welcome_send_message(UserWelcomeSchema(**data).user_id)

    async def run(self):
        await self.sender.connect()
        await self.rabbit.consume(self.queue, self.handling_message)
        await self.sender.disconnect()
