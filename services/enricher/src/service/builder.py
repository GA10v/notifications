from abc import ABC, abstractmethod
from typing import Any

from models.events import Event
from service.enrich.handler import get_payload


class BuilderProtocol(ABC):
    @abstractmethod
    async def build(self, data: dict[str, Any], **kwargs) -> str:
        ...


class BuilderService(BuilderProtocol):
    async def build(self, data: dict[str, Any], **kwargs) -> dict:
        print('ok')  # noqa: T201
        event = Event(**data)
        print('event: ', event)  # noqa: T201
        payload = await get_payload(event)  # noqa: F841
        return {'msg': 'test-ok'}
