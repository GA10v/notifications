"""Module to use to send email."""

import smtplib
from email.message import EmailMessage

from core.config import settings
from v1.workers.generic_worker import Worker


class EmailWorker(Worker):
    """Mail Worker Logic."""

    def __init__(self) -> None:
        """Create instance of MAILWorker."""
        self.server = settings.email.SMTP_SERVER
        self.port = settings.email.SMTP_PORT
        self.user = settings.email.USER
        self.password = settings.email.PASSWORD
        self.connection: smtplib.SMTP | smtplib.SMTP_SSL
        if settings.email.SMTP_SSL:
            self.connection = smtplib.SMTP_SSL(self.server, self.port)
        else:
            self.connection = smtplib.SMTP(self.server, self.port)
        self.connection.login(self.user, self.password)

    def send_message(
        self,
        message_to_send: dict,
    ) -> None:
        """Send emails.

        Args:
            message: dict - includes reciepents, subject and body
        """
        recipient = message_to_send.get('recipient')
        message_body = message_to_send.get('message_body')

        message = EmailMessage()
        message['From'] = settings.email.USER
        message['To'] = settings.email.USER
        message['Subject'] = message_to_send.get('subject')
        message.add_alternative(message_body, subtype='html')
        self.connection.sendmail(settings.email.USER, recipient, message.as_string())
        self.connection.close()


if __name__ == '__main__':
    fields = {
        'text': 'Произошло что-то интересное',
        'image': 'https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7-96e1c2d387fa.png',
    }
    mail_worker = EmailWorker()
    mail_worker.send_message(
        ['Павел Захаров <zpe25@yandex.ru>'],
        'Привет!',
        'mail.html',
        fields,
    )
