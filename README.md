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


$ docker compose exec -it url_shortener bash
root@50f2bf89c599:/opt/app# flask -A shortener_service.wsgi_app:app db init
Error: Directory migrations already exists and is not empty
root@50f2bf89c599:/opt/app# flask -A shortener_service.wsgi_app:app db migrate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'short_url'
  Generating /opt/app/migrations/versions/dabf0be0e01a_.py ...  done
root@50f2bf89c599:/opt/app# flask -A shortener_service.wsgi_app:app db upgrade
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> dabf0be0e01a, empty message
