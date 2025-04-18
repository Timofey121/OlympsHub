# OlympsHub

**OlympsHub** — программный комплекс для предоставления информации о школьных олимпиадах. Состоит из трёх основных компонентов:

1. **Site** — веб‑приложение на Django  
2. **TelegramBot** — бот в Telegram для рассылки уведомлений  
3. **nginx** — обратный прокси и статический сервер  
4. Вспомогательные сервисы: PostgreSQL, Redis, Celery, Flower  

---

## 📂 Структура проекта

```
OlympsHub/
├── Site/                 # Django‑приложение
│   ├── manage.py
│   ├── Site/             # внутренний пакет Django
│   └── requirements.txt
├── TelegramBot/          # Telegram‑бот
│   ├── main_olympiads.py
│   └── requirements.txt
├── nginx/                # Конфигурация nginx
│   ├── Dockerfile
│   └── default.conf
├── .env.db               # Настройки подключения к БД
├── docker-compose.yml    # Описание всех сервисов
└── README.md             # Этот файл
```

---

## 🚀 Быстрый старт

1. **Клонируйте репозиторий**  
   ```bash
   git clone https://github.com/Timofey121/OlympsHub.git
   cd OlympsHub
   ```

2. **Создайте и заполните `.env`‑файлы**  
   - `./.env.db` — параметры PostgreSQL (смотрите пример в репо)  
   - `./Site/.env.site` — секретный ключ Django, DEBUG, ALLOWED_HOSTS и прочие  
   - `./TelegramBot/.env.tg` — токен Telegram‑бота и настройки  

3. **Запустите все сервисы через Docker Compose**  
   ```bash
   docker-compose up --build -d
   ```

4. **Выполните миграции и создайте суперпользователя**  
   ```bash
   # откроется shell контейнера Django
   docker-compose exec django python manage.py migrate
   docker-compose exec django python manage.py createsuperuser
   ```

5. **Проверьте работу**  
   - Веб‑интерфейс: http://localhost/  
   - Админка Django: http://localhost/admin/  
   - Telegram‑бот: найдите его по токену в вашем Telegram  

---

## 🖥️ Описание сервисов

### 1. PostgreSQL  
- Запускается из образа `postgres:15`  
- Данные лежат в volume `postgres_data`  

### 2. Django (**Site**)  
- Контейнер `django`  
- Порт `8000` → `gunicorn`  
- Хранит: список и описание олимпиад, пользовательские аккаунты, админ‑панель  

### 3. Redis + Celery  
- Контейнеры `redis`, `worker`, `beat`  
- Асинхронная обработка задач (рассылка уведомлений, парсинг новых олимпиад)  
- Мониторинг задач через **Flower** (порт `5555`)  

### 4. TelegramBot  
- Контейнер `bot`  
- Файл запуска `main_olympiads.py`  
- Подписан на события Celery/Redis, рассылка уведомлений участникам  

### 5. nginx  
- Обратный прокси для Django, SSL (Let's Encrypt)  
- Сервирует статику и медиа из томов `static_volume`, `media_volume`  

---

## 🔧 Окружение и переменные

- **`.env.db`**  
  ```dotenv
  SQL_ENGINE=django.db.backends.postgresql
  POSTGRES_USER=timofey
  POSTGRES_PASSWORD=...
  POSTGRES_HOST=postgres
  POSTGRES_DB=olympshub
  POSTGRES_PORT=5432
  ```

- **`Site/.env.site`** (пример)  
  ```dotenv
  SECRET_KEY=ваш_секретный_ключ
  DEBUG=False
  ALLOWED_HOSTS=localhost,your-domain.com
  DATABASE_URL=postgres://timofey:...@postgres:5432/olympshub
  ```

- **`TelegramBot/.env.tg`** (пример)  
  ```dotenv
  TELEGRAM_TOKEN=ваш_бот_токен
  ```

---

## 📈 Мониторинг и логирование

- **Flower**: http://localhost:5555  
- Логи Docker:  
  ```bash
  docker-compose logs -f django
  docker-compose logs -f bot
  docker-compose logs -f worker
  ```

---

## 🤝 Вклад и поддержки

1. Форкните репозиторий  
2. Создайте ветку `feature/…` или `bugfix/…`  
3. Напишите код и тесты  
4. Откройте Pull Request  

---

> **Контакты**  
> Timofey121 — ale3jurtaev@gmail.com  
