# Warehouse Management System API

![Python](https://img.shields.io/badge/python-3.12+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-blue?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-orange?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-purple?style=for-the-badge&logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-green?style=for-the-badge)

REST API для управления складскими операциями с использованием FastAPI.   
Позволяет управлять товарами, запасами и
заказами с автоматической проверкой доступности товаров.

---

## ✨ Особенности

- Полный CRUD для товаров и заказов
- Автоматическое резервирование товаров при создании заказа
- Валидация данных через Pydantic v2
- Асинхронное взаимодействие с базой данных
- Поддержка статусов заказов с конечным автоматом
- Интеграция с PostgreSQL через SQLAlchemy 2.0 Async
- Готовые миграции Alembic
- Полностью покрыт тестами (unit + интеграционные)

---

## 🛠 Технологический стек

- **Язык**: Python 3.12+
- **Фреймворк**: FastAPI 0.115+
- **ORM**: SQLAlchemy 2.0 (Async)
- **БД**: PostgreSQL + asyncpg
- **Валидация**: Pydantic v2
- **Миграции**: Alembic
- **Зависимости**: Poetry
- **Тестирование**: pytest + HTTPX

---

## ⚡ Быстрый старт

### Предварительные требования

- Python 3.12+
- PostgreSQL 14+
- Poetry 1.6+
- SQLAlchemy 2.0+ (async)

### Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/dimais77/wms-api.git
cd WarehouseManagementSystemAPI/wms_app
```

2. Установить зависимости:

```bash
poetry install
```

3. Настроить окружение:

```bash
cp .env.template .env
```

Отредактируйте `.env`:

```ini
APP_CONFIG__DB__URL=postgresql+asyncpg://user:pwd@localhost:5432/wms_db
APP_CONFIG__DB__ECHO=false
```

4. Инициализировать БД:

```bash
alembic upgrade head
```

5. Запустить сервер:

```bash
poetry run uvicorn main:app --reload
```

Документация API будет доступна по адресу:  
http://localhost:8000/docs

---

## 🗂 Структура проекта

```text
.
├── LICENSE
├── README.md
├── compose.yaml
├── poetry.lock
├── pyproject.toml
└── wms-app/
    ├── alembic/              # Миграции базы данных
    ├── alembic.ini
    ├── api/
    │   └── v1/              # Версия API
    ├── core/                # Базовые настройки
    ├── db/                  # Работа с БД
    ├── dto/                 # Data Transfer Objects
    ├── main.py
    ├── models/
    │   └── mixins/          # Миксины для моделей
    ├── pytest.ini
    ├── repositories/        # Паттерн Repository
    ├── schemas/             # Pydantic схемы
    ├── services/            # Бизнес-логика
    ├── tests/
    └── utils/               # Вспомогательные утилиты
```

---

## 📚 Документация API

### Товары (`/api/v1/products`)

| Метод  | Эндпоинт        | Описание                 |
|--------|-----------------|--------------------------|
| GET    | `/`             | Получить все товары      |
| GET    | `/{product_id}` | Получить товар по ID     |
| POST   | `/`             | Создать новый товар      |
| PUT    | `/{product_id}` | Полное обновление товара |
| DELETE | `/{product_id}` | Удалить товар            |

### Заказы (`/api/v1/orders`)

| Метод | Эндпоинт             | Описание               |
|-------|----------------------|------------------------|
| GET   | `/`                  | Все заказы             |
| GET   | `/{order_id}`        | Заказ по ID            |
| POST  | `/`                  | Создать заказ          |
| PATCH | `/{order_id}/status` | Обновить статус заказа |

**Статусы заказа**:

- `draft` (черновик)
- `pending` (в обработке)
- `shipped` (отправлен)
- `delivered` (доставлен)

---

## 🧪 Тестирование

Запуск тестов:

```bash
poetry run pytest -v
```

Запуск тестов с покрытием:

```bash
poetry run pytest --cov=wms_app --cov-report=html
```

Структура тестов:

- `tests/api/` - интеграционные тесты API

---

## 🔒 Безопасность

- Валидация всех входных данных через Pydantic
- Автоматическая обработка ошибок SQLAlchemy
- Транзакционное выполнение операций с БД

---

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности смотрите в файле [LICENSE](LICENSE).

---

## ✉️ Контакты

Дмитрий Исаев:

- Telegram: [@dimais77](https://t.me/dimais77)
- Email: [dimais@mail.ru](mailto:dimais@mail.ru)

Проект доступен по адресу:  
https://github.com/dimais77/wms-api.git

```