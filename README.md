# Настройка проекта YaMDB для запуска в контейнере
### Описание
Проект YaMDb собирает отзывы пользователей на произведения.

В данном проекте при пуше проекта на GitHub выполняется:
- Тестирование проекта (выполнение автоматических тестов)
- Сборка приложения в контейнер Docker и размещение его на Docker hub
- Деплой проекта на сервере
- Отправка сообщения в телеграм при успешном деплое проекта.
-


![example workflow](https://github.com/Ilyako78/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


### Ссылка на документцию

http://yamdb.mikonsgame.ru/redoc/


### Стек технологий

Python 3.7

Django REST framework

Django ORM

Docker

Gunicorn

nginx

PostgreSQL

Git

GitHub Actions

### Шаблон файла .env

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql

DB_NAME= # имя базы данных

POSTGRES_USER= # логин для подключения к базе данных

POSTGRES_PASSWORD= # пароль для подключения к БД (установите свой)

DB_HOST=db # название сервиса (контейнера)

DB_PORT=5432 # порт для подключения к БД

### Запуск проекта в контейнере

docker compose up -d --build

docker compose exec web python manage.py migrate

docker compose exec web python manage.py createsuperuser

docker compose exec web python manage.py collectstatic --no-input

### Сделать резервную копию

docker compose exec web python manage.py dumpdata > fixtures.json

### Восстановить из резервной копии

docker cp fixtures.json <имя контейнера>:app/

docker compose exec web python manage.py loaddata fixtures.json

## Файлы настроек

Nginx:
infra/nginx/default.conf

Docker:
api_yamdb/Dockerfile

Docker compose:
infra/docker-compose.yaml

Workflow:
.github/workflows/yamdb_workflow.yml

## Примеры
Полная спецификация api
```
/redoc/
```

Запрос кода подтверждения при регистрации
```
/api/v1/auth/signup/
```

Получение JWT-токена
```
/api/v1/auth/token/
```

Получение списка всех категорий
```
/api/v1/categories/
```

Получение списка всех произведений
```
/api/v1/titles/
```

Загрузить данные из csv файлов:
```
python3 manage.py upload_db
```

## Авторы

https://github.com/Ilyako78

