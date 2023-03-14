import logging

from celery import shared_task  # type: ignore[attr-defined]
from services.generator.src.service.main import EventType, ProcessTask, Task

logger = logging.getLogger(__name__)


@shared_task(name='create_new_content_task')
def create_new_content_task(*args, **kwargs):
    task = Task(event_type=EventType.new_content, context=kwargs)
    generator = ProcessTask()
    generator.perform_task(task)
