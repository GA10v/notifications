from models.events import Event
from models.payloads import NewUserContext
from service.enrich.protocol import PayloadsProtocol


class NewUserPayload(PayloadsProtocol):
    def __init__(self, data: Event) -> None:
        self.data = data

    async def payload(self) -> NewUserContext:
        return NewUserContext(
            user_name=self.data.context.name,
            email=self.data.context.email,
            link='TODO добавить короткие ссылки',
            delivery_type='email',
        )
