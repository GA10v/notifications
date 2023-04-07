import logging

from celery import shared_task  # type: ignore[attr-defined]

from generator.src.service.main import ProcessTask  # noqa: F401
from generator.src.models.task import Task
from generator.src.models.base import EventType

logger = logging.getLogger(__name__)


@shared_task(name='Создать задачу new_content')
def create_new_content_task(*args, task_id: str, **kwargs):
    # task = Task(event_type=EventType.new_content, context=kwargs)  # noqa: E800
    generator = ProcessTask()
    task = generator.get_task(task_id)
    logger.info(f'task: {task}')
    generator.perform_task(task)


@shared_task(name='Создать задачу new_promo')
def create_new_promo_task(*args, task_id: str, **kwargs):
    # task = Task(event_type=EventType.promo, context=kwargs)  # noqa: E800
    generator = ProcessTask()
    task = generator.get_task(task_id)
    logger.info(f'task: {task}')
    generator.perform_task(task)


@shared_task(name='Создать задачу new_likes')
def create_new_likes_task(*args, task_id: str, **kwargs):
    logger.info(f'"task_id": {task_id}, "kwargs": {kwargs}')
    generator = ProcessTask()
    generator.perform_task(generator.get_task(task_id))


@shared_task(bind=True, name='Debug')
def hello_world(self):
    print('Hi ========================')  # noqa: T201
