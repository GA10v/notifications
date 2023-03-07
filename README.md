# Проектная работа 10 спринта

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