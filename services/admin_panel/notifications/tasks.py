import logging

from celery import shared_task  # type: ignore[attr-defined]
from services.generator.src.service.main import ProcessTask

logger = logging.getLogger(__name__)


@shared_task(name='hello')
def hello():
    task = None
    logger.debug('Hello there!')
    new_task = ProcessTask()
    new_task.perform_task(task)
