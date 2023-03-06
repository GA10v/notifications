"""Module to use to send email."""

import pathlib
import smtplib
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader, select_autoescape

from sender.settings.config import Settings
from sender.v1.workers.generic_worker import Worker

settings = Settings()


class EmailWorker(Worker):
    """Mail Worker Logic."""

    def __init__(self) -> None:
        """Create instance of MAILWorker."""
        self.server = settings.email_smtp_server
        self.port = settings.email_smtp_port
        self.user = settings.email_user
        self.password = settings.email_password
        self.connection: smtplib.SMTP | smtplib.SMTP_SSL
        if settings.email_smtp_ssl:
            self.connection = smtplib.SMTP_SSL(self.server, self.port)
        else:
            self.connection = smtplib.SMTP(self.server, self.port)
        self.connection.login(self.user, self.password)

    def send_message(
        self,
        recipients: list[str],
        subject: str,
        template: str,
        fields: dict[str, str],
    ) -> None:
        """Send emails.

        Args:
            recipients: list - List of email reciepents
            subject: str - Subject of email
            template: str - Template to compose email body
            fields: dict - Fields to fill the template
        """
        message = EmailMessage()
        message['From'] = settings.email_user
        message['To'] = settings.email_user
        message['Subject'] = subject

        templates_storage = pathlib.Path() / 'templates'
        env = Environment(
            loader=FileSystemLoader(templates_storage),
            autoescape=select_autoescape(),
        )
        template_rendered = env.get_template(template).render(
            title=subject,
            **fields,
        )
        message.add_alternative(template_rendered, subtype='html')
        self.connection.sendmail(settings.email_user, recipients, message.as_string())
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
