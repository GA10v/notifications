import json
from contextlib import suppress

import asyncclick as click
from trio_websocket import ConnectionClosed, serve_websocket

from settings.config import settings
from v1.workers.generic_worker import Worker


class WebSocketWorker(Worker):
    def __init__(self):
        self.settings = settings

    def send_message(self, recipients, subject, template, fields):
        # Save state to database for request by user
        pass


async def notification_server(request):
    ws = await request.accept()
    while True:
        try:
            message = await ws.get_message()
            if message.lower() == 'list_notifications':
                # getting list notifications
                messages_list = []
                await ws.send_message(json.dumps(messages_list))
                continue
        except ConnectionClosed:
            break


@click.command()
@click.option('--port', default=8000, help='Port to listen')
@click.option('--ip', default='127.0.0.1', help='Address to use')
async def main(port: int, ip: str):
    await serve_websocket(
        notification_server,
        ip,
        port,
        ssl_context=None,
    )


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        main(_anyio_backend='trio')
