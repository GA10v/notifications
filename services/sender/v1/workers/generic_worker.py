"""Class to implement late."""
import abc


class Worker(abc.ABC):
    """Class to implement."""

    @abc.abstractmethod
    def send_message(
        self,
        recipients: list[str],
        subject: str,
        template: str,
        fields: dict[str, str],
    ) -> None:
        """Send general message.

        Args:
            recipients: list - List of email reciepents
            subject: str - Subject of email
            template: str - Template to compose email bodys
            fields: dict - Dictionary with fields to fill in template

        Raises:
            NotImplementedError: abstract instance
        """
        raise NotImplementedError
