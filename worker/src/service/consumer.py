import json

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


class Worker(RabbitBase):
    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        try:
            print(data)
        except:
            self._open().stop_consuming()
            self.start()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        print('start')
        channel = self._open()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_consume(self.queue, self.callback)
        channel.start_consuming()


if __name__ == '__main__':
    Worker(settings.rabbit.QUEUE_1).start()
