from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import Response

from core.config import settings
from utils.auth import parse_header


def auth_middleware(app: FastAPI) -> None:
    @app.middleware('http')
    async def check_jwt(request: Request, call_next: Any) -> Any:
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return Response('Authorization header is missing', HTTPStatus.UNAUTHORIZED)
        claims = parse_header(auth_header)['claims']
        if claims.get('is_super'):
            return await call_next(request)

        produce_path = f'{settings.fastapi.HOST}:{settings.fastapi.PORT}/{settings.fastapi.PREFIX}/send'
        if produce_path in str(request.url):
            if settings.permission.User in claims.get('permissions'):
                return await call_next(request)
            return Response('Permission denied', HTTPStatus.FORBIDDEN)
