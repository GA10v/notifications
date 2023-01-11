from abc import ABC, abstractmethod
from email.message import EmailMessage
from pathlib import Path

from aiosmtplib import SMTP, SMTPException
from workers.src.core.config import settings
from jinja2 import Environment, FileSystemLoader


class SenderProtocol(ABC):
    @abstractmethod
    async def send(self, data) -> bool:
        ...

    @abstractmethod
    async def connect(self):
        ...

    @abstractmethod
    async def disconnect(self):
        ...


class EmailSender(SenderProtocol):
    def __init__(
        self,
        host: str = settings.smtp.HOST,
        port: int = settings.smtp.PORT,
        user: str = settings.smtp.USER,
        password: str = settings.smtp.PASSWODR,
    ) -> None:
        self.user = user
        self.password = password
        self.client = SMTP(hostname=host, port=port)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.quit()

    async def _connect(self) -> bool:
        if not self.client.is_connected:
            await self.client.connect()
        return self.client.is_connected

    async def send(self, data: dict) -> bool:
        msg = EmailMessage()
        msg['From'] = settings.smtp.USER
        msg['To'] = data.get('email')
        msg['Subject'] = data.get('subject')

        env = Environment(loader=FileSystemLoader(Path(Path(__file__).parent.parent, 'templates')))
        template = env.get_template(f'{data.get("template")}.html')
        output = template.render(**data.get('payload'))
        msg.add_alternative(output, subtype='html')
        try:
            if await self._connect():
                await self.client.sendmail(
                    sender=settings.smtp.USER,
                    recipients=[data.get('email')],
                    message=msg.as_string(),
                )
        except SMTPException:
            return False
        return True
