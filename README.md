# OpenSearchPy

**OpenSearchPy** - это веб-приложение для работы с **OpenSearch**, позволяющее:
- Создавать индекс с полями:
  - `title` (текст)
  - `content` (текст)
  - `content_type` (одно из 4 значений)
- Загружать в индекс тестовые документы.
- Искать документы по ключевому слову в `title` и `content`.
- Возвращать список с полями:
  - `title`
  - `snippet` — первые 50 символов из `content`
- Фильтровать результаты поиска по `content_type`.

___

## Стек технологий
```txt
- Python 3.13
- FastAPI
- Faker
- OpenSearch Python Client
- Uvicorn
- Docker / Docker Compose
- OpenSearch (через Docker)
```

## Структура проекта

```txt
├── core
│   ├── config.py              # Настройки подключения
│   ├── models.py              # Модели
│   └── opensearch_client.py   # Логика работы с OpenSearch
├── main.py                    # Точка входа FastAPI
├── docker-compose.yml         # Запуск OpenSearch и приложения
├── requirements.txt           # Зависимости проекта
└── .env                       # Переменные окружения
```

## Запуск проекта

### 1. Клонируем репозиторий

```bash
git clone https://github.com/A737580/openSearchPy.git
cd openSearchPy
```

### 2. Запускаем через Docker Compose

```bash
docker-compose up -d
```

### 3. Запускаем Web-сервер

```bash
python main.py
```

Это поднимет:

* OpenSearch
* OpenSearch Dashboards (по адресу [http://localhost:5601](http://localhost:5601))
* FastAPI-приложение (по адресу [http://localhost:8000](http://localhost:8000))


## 📡 Эндпоинты API

```http
POST /load_data
    Описание: добавляет случайные данные в хранилище Opensearch по 5 шт за запрос
GET /search
    Query параметры:
      - query: str — ключевое слово для поиска
      - content_type: str — фильтр по типу контента
    Ответ:
      [
        {
          "title": "Example",
          "snippet": "Lorem ipsum dolor sit amet, conse..."
        }
      ]
GET    /docs           
        Описание: документация swagger - веб интерфейс для работы с апи
GET    /http://localhost:5601
        Описание: OpenSearch Dashboards - альтернативный веб интерфейс для администирования хранилища OpenSearch
```

