import uvicorn
from config import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from utils import get_fake_review_info

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.post('/ugc/v1/review_info/{movie_id}/{user_id}/{review_id}')
async def review_info(movie_id: str, user_id: str, review_id: str):
    return get_fake_review_info(movie_id, user_id, review_id)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8083)
