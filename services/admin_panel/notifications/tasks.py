import logging

from celery import shared_task  # type: ignore[attr-defined]

logger = logging.getLogger(__name__)


@shared_task(name='hello')
def hello():
    logger.debug('Hello there!')
