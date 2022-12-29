import uvicorn

from app.src.api.v1 import notific
from app.src.core.config import settings
from fastapi import FastAPI
# from fastapi.responses import ORJSONResponse

from app.src.service.producer import init_queue


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    # default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup() -> None:
    await init_queue()


@app.on_event('shutdown')
async def shutdown() -> None:
    print('shutdown')


app.include_router(notific.router, prefix=settings.fastapi.NOTIFIC_PREFIX, tags=['notification'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080)
