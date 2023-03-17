import json
import logging
from contextlib import suppress

import asyncclick as click
import trio
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from trio_websocket import ConnectionClosed, WebSocketRequest, serve_websocket
from v1.workers.generic_worker import Worker

from core.config import settings
from models.db.notifications import Notification
from models.notifications import TemplateToSender

WEBSOCKET_CHECK_TIMEOUT = 10

logger = logging.getLogger(__name__)


class WebSocketWorker(Worker):
    def __init__(self) -> None:
        self.settings = settings
        self.engine = create_engine(self.settings.postgres.uri)

    def send_message(self, notification: TemplateToSender) -> None:
        with Session(self.engine) as session:
            notification_object = Notification(
                id=notification.notification_id,
                user_id=notification.user_id,
                ws_body=notification.ws_body,
                subject=notification.subject,
            )
            session.add(notification_object)
            session.commit()


async def notification_server(request: WebSocketRequest) -> None:
    engine = create_engine(settings.postgres.uri)
    ws = await request.accept()
    # getting user_id
    user_id = None
    while True:
        try:
            with trio.move_on_after(WEBSOCKET_CHECK_TIMEOUT):
                message = await ws.get_message()
                if message.lower() == 'list_notifications':
                    stmt = select(Notification).filter_by(user_id=user_id)
                    with Session(engine) as session:
                        messages_list = [obj.as_dict() for obj in session.execute(stmt).scalars.all()]
                    await ws.send_message(json.dumps(messages_list))
            continue
        except ConnectionClosed:
            break


@click.command()
@click.option('--port', default=8000, help='Port to listen')
@click.option('--ip', default='127.0.0.1', help='Address to use')
async def main(port: int, ip: str) -> None:
    await serve_websocket(
        notification_server,
        ip,
        port,
        ssl_context=None,
    )


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        main(_anyio_backend='trio')
