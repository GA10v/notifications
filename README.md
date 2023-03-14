# Проектная работа 10 спринта

TODO: Оформить документацию

## Запуск

1. Установить зависимости командой
   `$ poetry install`
2. Создать файл конфигурации `.env` в корне проекта и заполнить его согласно `example.env`
3. Запустить контейнер командой
   `$ docker-compose up`
4. Cервис API запускается командой
   `$ python3 services/notific_api/src/main.py`
5. Сервис enricher запускается командой
   `$ python3 services/enricher/src/main.py`
6. Перейти к документации Admin_panel по url: `http://localhost:8000/admin`(USER='asdmin', PASSWORD='admin')
7. Перейти к документации API по url: `http://localhost:8080/api/openapi`
8. Перейти к документации Mock_Auth по url: `http://localhost:8081/api/openapi`
9. Перейти к документации Mock_Admin_panel по url: `http://localhost:8082/api/openapi`
10. Перейти к документации Mock_ugc по url: `http://localhost:8083/api/openapi`
11. Перейти к документации RabbitMQ по url: `http://localhost:15672/` (USER='guest', PASSWORD='guest')
