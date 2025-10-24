# Spy & See - Сервис уведомлений

Микросервис для управления уведомлениями пользователей, построенный на FastAPI с использованием PostgreSQL и Tortoise ORM.

## 🚀 Возможности

- **Аутентификация пользователей**: регистрация и авторизация с JWT токенами
- **Управление уведомлениями**: создание, получение и удаление уведомлений
- **Типы уведомлений**: лайки, комментарии, репосты
- **RESTful API**: полная документация через Swagger UI
- **Docker контейнеризация**: готовый к развертыванию

## 🏗️ Архитектура

Проект следует принципам чистой архитектуры с разделением на слои:

```
src/
├── main.py                 # Точка входа приложения
├── dependencies.py         # Зависимости FastAPI
├── validators.py          # Валидаторы данных
├── requirements.txt       # Python зависимости
├── models/
│   ├── api/              # API модели (Pydantic)
│   ├── core/             # Бизнес-логика
│   └── db/               # Модели базы данных (Tortoise ORM)
└── routers/              # API маршруты
    ├── auth.py           # Аутентификация
    └── notifications.py  # Уведомления
```

## 🛠️ Технологический стек

- **FastAPI** - веб-фреймворк
- **Tortoise ORM** - асинхронная ORM
- **PostgreSQL** - база данных
- **JWT** - аутентификация
- **Docker** - контейнеризация
- **Pydantic** - валидация данных

## 📋 Требования

- Python 3.12+
- Docker и Docker Compose
- PostgreSQL (через Docker)

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/pmswga/notify-api.git
```

```bash
cd spy&see
```

### 2. Настройка переменных окружения

Создайте файл `.env` в папке `src/`:

```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Запуск через Docker Compose

```bash
docker-compose up --build
```

Сервис будет доступен по адресу: http://localhost:80

## 📚 API Документация

После запуска приложения документация доступна по адресам:

- **Swagger UI**: http://localhost/docs
- **ReDoc**: http://localhost/redoc

## 🔐 API Endpoints

### Аутентификация (`/auth`)

- `POST /auth/register` - Регистрация нового пользователя
- `POST /auth/login` - Авторизация пользователя
- `POST /auth/refresh` - Обновление токенов

### Уведомления (`/notification`)

- `POST /notification/notifications` - Создание уведомления
- `GET /notification/notifications` - Получение всех уведомлений пользователя
- `DELETE /notification/notifications/{id}` - Удаление уведомления

## 📊 Модели данных

### Пользователь (UserDB)
- `id` - уникальный идентификатор
- `username` - имя пользователя (уникальное)
- `avatar_url` - URL аватара
- `created_at` - дата создания

### Уведомление (NotificationDB)
- `id` - уникальный идентификатор
- `user_id` - ID пользователя
- `type` - тип уведомления (LIKE, COMMENT, REPOST)
- `text` - текст уведомления
- `created_at` - дата создания

### Токены (TokenDB)
- `user_id` - ID пользователя
- `access` - access токен
- `refresh` - refresh токен

## 🔧 Типы уведомлений

```python
class NotificationType(IntEnum):
    LIKE = 0      # Лайк
    COMMENT = 1   # Комментарий
    REPOST = 2    # Репост
```

## 🐳 Docker сервисы

- **api** - основное приложение (порт 80)
- **database** - PostgreSQL (порт 5432)
- **adminer** - веб-интерфейс для БД (порт 8080)

## Дальнейшие планы

- Наисание тестов
- Написание миграций
- Доработка аутентификации
