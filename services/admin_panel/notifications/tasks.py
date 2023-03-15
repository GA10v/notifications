import logging

from celery import shared_task  # type: ignore[attr-defined]

from admin_panel.generator.src.service.main import EventType, ProcessTask, Task

logger = logging.getLogger(__name__)


@shared_task(name='Создать задачу new_content')
def create_new_content_task(*args, **kwargs):
    task = Task(event_type=EventType.new_content, context=kwargs)
    generator = ProcessTask()
    generator.perform_task(task)


@shared_task(name='Создать задачу new_promo')
def create_new_promo_task(*args, **kwargs):
    task = Task(event_type=EventType.promo, context=kwargs)
    generator = ProcessTask()
    generator.perform_task(task)


@shared_task(name='Создать задачу new_likes')
def create_new_likes_task(*args, **kwargs):
    task = Task(event_type=EventType.new_likes, context=kwargs)
    generator = ProcessTask()
    generator.perform_task(task)
