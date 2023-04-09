import logging

from celery import shared_task  # type: ignore[attr-defined]

from generator.src.service.main import ProcessTask  # noqa: F401

logger = logging.getLogger(__name__)


@shared_task(name='Создать задачу new_content')
def create_new_content_task(*args, task_id: str, **kwargs):
    logger.info(f'New content task. Args: {args}, task_id: {task_id}, kwargs: {kwargs}')
    generator = ProcessTask()
    generator.perform_task(generator.get_task(task_id))


@shared_task(name='Создать задачу new_promo')
def create_new_promo_task(*args, task_id: str, **kwargs):
    logger.info(f'New promo task. Args: {args}, task_id: {task_id}, kwargs: {kwargs}')
    generator = ProcessTask()
    generator.perform_task(generator.get_task(task_id))


@shared_task(name='Создать задачу new_likes')
def create_new_likes_task(*args, task_id: str, **kwargs):
    logger.info(f'New likes task. Task_id: {task_id}, kwargs: {kwargs}')
    generator = ProcessTask()
    generator.perform_task(generator.get_task(task_id))


@shared_task(bind=True, name='Debug')
def hello_world(self):
    print('Hi ========================')  # noqa: T201
