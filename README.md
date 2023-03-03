# Проектная работа 10 спринта

## Стандартный запуск
Установка переменных из файла .env.example в файл .env

```
docker compose up -d --build
docker compose exec -it admin-panel bash
python manage.py collectstatic
python manage.py migrate
python manage.py createsuperuser
```