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
6. Mock сервиса Auth запускается командой
    ```$ python3 mock/auth/main.py```
7. Mock сервиса Admin_panel запускается командой
    ```$ python3 mock/admin_panel/main.py```
8. Mock сервиса UGC запускается командой
    ```$ python3 mock/ugc/main.py```
9. Перейти к документации API по url: ```http://localhost:8080/api/openapi```
10. Перейти к документации Mock_Auth по url: ```http://localhost:8081/api/openapi```
11. Перейти к документации Mock_Admin_panel по url: ```http://localhost:8082/api/openapi```
12. Перейти к документации Mock_ugc по url: ```http://localhost:8083/api/openapi```
13. Перейти к документации RabbitMQ по url: ```http://localhost:15672/``` (USER='guest', PASSWORD='guest')