gunicorn -w 4 -b 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker app.src.main:app
cd ./app/src
alembic upgrade head
