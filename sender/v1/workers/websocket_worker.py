from settings.config import settings
from v1.workers.generic_worker import Worker


class WebSocketWorker(Worker):
    def __init__(self):
        self.settings = settings
