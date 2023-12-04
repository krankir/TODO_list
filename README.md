# TODO list
## Описание
RESTful API для работы с TODO-листом и регистрацией и авторизацией

### Технологии
- Python
- Postgresql
- Django REST Framework
- Docker

### Шаблон наполнения .env файла
- работаем с postgresql
```
DB_ENGINE=django.db.backends.postgresql 
```
- имя базы данных
```
DB_NAME=postgres
```
- пользователь базы данных
```
POSTGRES_USER=postgres
```
- пароль пользователя базы данных
```
POSTGRES_PASSWORD=postgres
```
- название контейнера
```
DB_HOST=db
```
- порт для работы с базой данных
```
DB_PORT=5432
```

### Запуск проекта в контейнерах Docker
- Перейдите в раздел infra для сборки docker-compose
```
docker-compose up -d --build 
```
- Выполнить migrate
```
docker-compose exec web python manage.py migrate
```
- Создайте пользователя
```
docker-compose exec web python manage.py createsuperuser
```
- (или) Сменить пароль для пользователя admin
```
docker-compose exec web python manage.py changepassword admin
```
- Сформируйте STATIC файлы:
```
docker-compose exec web python manage.py collectstatic --no-input
```

# Реализованные API endpoints:
- **Регистрация пользователя**
```
Пользователь отправляет POST-запрос с параметром email, password и username на `api/v1/auth/users/`
```
- **Получение токена**
```
Пользователь отправляет POST-запрос с параметром в теде запроса "email": "", "password": "" 
на `api/auth/token/login/`
```
- **Действия требующие авторизации**
```
Пользователь отправляет GET-запрос с Headers ключом Authorization c значением Token <наш токен>
```
- **Получение списка задач пользователя.**
```
Полачать списки задач конкретных пользователей могут только пользователи с is_staff=True, username передаётся через 
параметр запроса имеем эндпоинт типа api/v1/tasks/?username=<username_пользователя> 
```
- **Создание задачи для пользователя**
```
Пользователь отправляет POST-запрос по эндпоинту api/v1/tasks/ с обязательным полем
в теле запроса "title": "<описание задачи>"
```
- **Получить задачу пользователя по ID задачи**
```
Пользователь отправляет GET-запрос по эндпоинту api/v1/tasks/ID/"
```
- **Удалить задачу пользователя**
```
Пользователь отправляет DELETE-запрос по эндпоинту api/v1/tasks/<ID удаляемой задачи>/"
```
- **Выполнить работу по задаче**
```
Пользователь отправляет PATCH-запрос по эндпоинту api/v1/work_complete/<ID выполняемой задачи>/"
с телом запроса "completed": "True"
```

### Все вводимые поля проверены на соответствие типам в соответствии с типами описанными в моделях.

### Автор
Анатолий Редько

### License
MIT
