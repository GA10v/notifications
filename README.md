# Проектная работа 10 спринта

TODO: Оформить документацию

## Стандартный запуск
Установка переменных из файла .env.example в файл .env

```
docker compose up -d --build
docker compose exec -it admin-panel bash
python manage.py collectstatic
python manage.py migrate
python manage.py createsuperuser
```


## Запуск
1. Установить зависимости командой
    ```$ poetry install```
2. Создать файл конфигурации ```.env``` в корне проекта и заполнить его согласно ```example.env ```
3. Запустить контейнер командой
    ```$ docker-compose up ```
4. Cервис API запускается командой
    ```$ python3 services/notific_api/src/main.py```
5. Сервис enricher запускается командой
    ```$ python3 services/enricher/src/main.py```
6. Перейти к документации API по url: ```http://localhost:8080/api/openapi```
7. Перейти к документации RabbitMQ по url: ```http://localhost:15672/``` (USER='guest', PASSWORD='guest')
