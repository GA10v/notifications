from core.config import settings
from service.consumer import Worker

if __name__ == '__main__':
    Worker(settings.rabbit.QUEUE_2).start()
