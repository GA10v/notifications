from abc import ABC, abstractmethod

from broker.rabbit import RabbitMQProducer, get_producer
from fastapi import Depends


class ProducerServiceProtocol(ABC):
    @abstractmethod
    async def send_event(self, payload: dict, **kwargs):
        ...


class RabbitMQProducerService(ProducerServiceProtocol):
    def __init__(self, producer: RabbitMQProducer) -> None:
        self.producer = producer

    async def send_event(self, payload: dict, **kwargs):
        return await self.producer.send_msg(msg=payload)


def get_producer_service(producer: RabbitMQProducer = Depends(get_producer)) -> RabbitMQProducerService:
    return RabbitMQProducerService(producer)
