from abc import ABC, abstractmethod
from email.message import EmailMessage
from pathlib import Path

from aiosmtplib import SMTP, SMTPException
from core.config import settings
from jinja2 import Environment, FileSystemLoader


class SenderProtocol(ABC):
    @abstractmethod
    async def send(self, data) -> bool:
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

    async def _connect(self) -> bool:
        if not self.client.is_connected:
            await self.client.connect()
            await self.client.login(username=self.user, password=self.password)
        return self.client.is_connected

    async def _disconnect(self):
        await self.client.quit()

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
                await self._disconnect()
        except SMTPException:
            return False
        return True
