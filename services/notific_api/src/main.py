import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import _notific, notific
from broker.rabbit import producer
from core.config import settings
from core.logger import LOGGING
from middleware.auth import auth_middleware
from middleware.logger import logging_middleware
from utils.sentry import init_sentry

init_sentry()

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

# middleware
logging_middleware(app=app)
if not settings.debug.DEBUG:
    auth_middleware(app=app)


@app.on_event('startup')
async def startup():
    await producer.init_producer(
        uri=settings.rabbit.uri,
        incoming_queue=settings.rabbit.QUEUE_TO_ENRICH.lower(),
        retry_queue=settings.rabbit.QUEUE_RETRY_ENRICH.lower(),
        incoming_exchange=settings.rabbit.EXCHENGE_INCOMING_1.lower(),
        retry_exchange=settings.rabbit.EXCHENGE_RETRY_1.lower(),
    )


@app.on_event('shutdown')
async def shutdown():
    await producer.connection.close()


app.include_router(notific.router, prefix=settings.fastapi.NOTIFIC_PREFIX, tags=['notification'])
app.include_router(_notific.router, prefix=settings.fastapi.NOTIFIC_PREFIX, tags=['test'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, log_config=LOGGING, log_level=logging.DEBUG)
