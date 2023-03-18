"""Module to use to send SMS."""

from v1.workers.generic_worker import Worker

from models.notifications import TemplateToSender


class SMSWorker(Worker):
    """Mail Worker Logic."""

    def __init__(self) -> None:
        """Create instance of MAILWorker."""
        ...

    def send_message(
        self,
        notification: TemplateToSender,
    ) -> None:
        """Send sms.

        Args:
            notification: TemplateToSender - includes reciepents, subject and body
        """
        raise NotImplementedError()
