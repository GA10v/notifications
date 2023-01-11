import asyncio
import json

import aio_pika
from pydantic import BaseModel

from workers.src.service.consumer import RabbitService
from workers.src.service.sender import SenderProtocol


class UserWelcome(BaseModel):
    user_id: str
    email: str
    login: str


class WelcomeWorker:
    def __init__(
        self,
        # pg_service,  #TODO
        rabbit_service: RabbitService,
        sender_service: SenderProtocol,
        queue_name: str,
    ) -> None:
        self.rabbit = rabbit_service
        # self.pg = pg_service #TODO
        self.sender = sender_service
        self.queue = queue_name

    @staticmethod
    async def _prepare_data(data):
        _data = UserWelcome(**data)
        data = {
            'subject': 'registration',
            'email': _data.email,
            'template': 'new_user',
            'payload': {
                'user_name': _data.login,
            },
        }
        return data

    async def handling_message(self, message: aio_pika.abc.AbstractIncomingMessage,):
        async with message.process():
            data = json.loads(message.body)
            send_data = await self._prepare_data(data)
            is_send = await self.sender.send(send_data)
        if is_send:
            # await self.pg.update_date()  #TODO
            ...

    async def run(self):
        await self.rabbit.consume(self.queue, self.handling_message)
        await self.sender.disconnect()
