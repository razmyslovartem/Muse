# 📔 Личный дневник

Веб-приложение для ведения личного дневника с возможностью создания, редактирования и удаления записей.

## 📋 Функционал

- ✅ Регистрация и аутентификация пользователей
- ✅ Создание, редактирование, удаление записей
- ✅ Просмотр списка всех записей
- ✅ Детальный просмотр записи
- ✅ Поиск по заголовку и содержимому
- ✅ Адаптивный дизайн с Bootstrap 5
- ✅ Админка Django

---

## 🚀 Стек технологий

| Технология | Назначение |
|------------|------------|
| Python 3.12 | Язык программирования |
| Django 6.0 | Веб-фреймворк |
| PostgreSQL 15 | База данных |
| Bootstrap 5 | UI-фреймворк |
| Docker / Docker Compose | Контейнеризация |
| Nginx | Веб-сервер / прокси |
| Gunicorn | WSGI-сервер |

### Дополнительно
- JWT авторизация для API
- Шифрование записей (cryptography)
- Тесты с покрытием 91%

## 🐳 Установка и запуск

### Через Docker (рекомендуется)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/razmyslovartem/Muse.git
cd Muse/diary-project

# 2. Создать .env файл
cp .env.example .env

# 3. Сгенерировать SECRET_KEY и ENCRYPTION_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# 4. Заполнить .env и nginx
в .env
#   - SECRET_KEY=сгенерированный_ключ
#   - ENCRYPTION_KEY=сгенерированный_ключ_шифрования
#   - ALLOWED_HOSTS=ваш_ip,localhost
#   - DB_PASSWORD=сложный_пароль
в docker/nginx/nginx.conf
#   - server_name localhost ваш айпи адрес сервера;

# 5. Собрать и запустить
docker compose up --build -d

# 6. Применить миграции
docker compose exec web poetry run python manage.py makemigrations
docker compose exec web poetry run python manage.py migrate

# 7. Создать суперпользователя
docker compose exec web poetry run python manage.py createsuperuser

# 8. Открыть в браузере
```

## 🖥 Локальный запуск (без Docker)

### Требования
- Python 3.12+
- Poetry (установка: `pip install poetry`)

### Установка зависимостей

```bash
# 1. Клонировать репозиторий
git clone https://github.com/razmyslovartem/Muse.git
cd Muse/diary-project

# 2. Установить Poetry (если не установлен)
pip install poetry

# 3. Установить зависимости
poetry install

# 4. Создать .env файл
cp .env.example .env
# Отредактировать .env (добавить SECRET_KEY, ENCRYPTION_KEY и т.д.)

# 5. Применить миграции
poetry run python manage.py makemigrations
poetry run python manage.py migrate

# 6. Создать суперпользователя
poetry run python manage.py createsuperuser

# 7. Запустить сервер
poetry run python manage.py runserver