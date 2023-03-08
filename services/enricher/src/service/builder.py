from abc import ABC, abstractmethod
from typing import Any


class BuilderProtocol(ABC):
    @abstractmethod
    async def build(self, data: dict[str, Any], **kwargs) -> str:
        ...


class BuilderService(BuilderProtocol):
    async def build(self, data: dict[str, Any], **kwargs) -> dict:
        print('OK')  # noqa: T201
        return {'msg': 'test-ok'}
