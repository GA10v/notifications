import asyncio

from core.config import settings
from pydantic import BaseModel

from .consumer import RabbitService
from .sender import SenderProtocol


class UserWelcome(BaseModel):
    user_id: str
    email: str
    login: str


class Worker:
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

    async def _prepare_data(self, data):
        if self.queue == settings.rabbit.QUEUE_1.lower():
            _data = UserWelcome(**data)
            link = ''  # TODO
            data = {
                'subject': 'registration',
                'email': _data.email,
                'template': 'new_user',
                'payload': {
                    'user_name': _data.login,
                    'link': link,
                },
            }
        elif self.queue == settings.rabbit.QUEUE_2:
            ...

        return data

    async def handling_message(self, data):
        send_data = await self._prepare_data(data)
        is_send = await self.sender.send(send_data)
        if is_send:
            # await self.pg.update_date()  #TODO
            ...

    async def work(self):
        tasks = []
        while data := await self.rabbit.consume(self.queue):
            tasks.append(asyncio.create_task(self.handling_message(data)))
        await asyncio.gather(*tasks)
