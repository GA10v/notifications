import pika
from app.src.core.config import settings


class RabbitBase:
    def __init__(self, queue: str) -> None:
        self.conn_params = pika.ConnectionParameters(settings.rabbit.HOST, settings.rabbit.PORT)
        self.connection = pika.BlockingConnection(self.conn_params)
        self.queue = queue.lower()

    def _open(self):
        return self.connection.channel()

    def _close(self):
        self.connection.close()
