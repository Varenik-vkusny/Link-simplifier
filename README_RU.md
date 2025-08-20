[Read in English](README.md)
---

# ✒️ Упроститель ссылки

[![Run Python Tests](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml/badge.svg)](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml)

Современное веб приложение с бэкендом на современном фреймворке FastAPI и клиентской частью в виде тг бота (aiogram 3) с дружественным интерфейсом.

---

## 🚀 О проекте

Этот проект является инструментом для упрощения длинных ссылок, он состоит из двух частей:

*   **REST API на FastAPI:** Высокоскоростной бэкенд на FastAPI, который управляет данными и обеспечивает безопасность данных пользователся при авторизации.
*   **Telegram-бот на aiogram 3:** Интерактивный клиент, который служит для работы с пользователем и получения от него команд и данных.

Проект демонстрирует навыки работы с асинхроннымм бэкендом и асинхронным тг ботом, а также навыки сборки приложения и написания тестов для него.

---

## 🛠️ Стек технологий

*   **Бэкенд:**
    *   ![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
    *   ![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?style=for-the-badge&logo=fastapi)
    *   ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-DB4437?style=for-the-badge&logo=sqlalchemy)
    *   ![Pydantic](https://img.shields.io/badge/Pydantic-2.0-E96F00?style=for-the-badge)
    *   ![Alembic](https://img.shields.io/badge/Alembic-migrations-4E2A84?style=for-the-badge)
*   **Telegram-бот:**
    *   ![aiogram](https://img.shields.io/badge/aiogram-3.x-26A5E4?style=for-the-badge)
    *   ![httpx](https://img.shields.io/badge/httpx-async-000000?style=for-the-badge)
*   **База данных:**
    *   ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-3-003B57?style=for-the-badge&logo=sqlite)
*   **Аутентификация и инструменты:**
    *   `python-jose` (JWT Tokens)
    *   `passlib` & `bcrypt` (Хэширование паролей)
    *   `Uvicorn` (ASGI-сервер)
    *   `python-dotenv` (Переменные окружения)
*   **Сборка приложения:**
    *   ![Docker](https://img.shields.io/badge/Docker-compose-2496ED?style=for-the-badge&logo=docker)
*   **Тесты:**
    *   ![Pytest](https://img.shields.io/badge/Pytest-testing-0A9EDC?style=for-the-badge&logo=pytest)

---

## ✨ Ключевые возможности

*   **Аутентификация и Авторизация:**
    *   🔐 Регистрация и вход пользователей по email/паролю.
    *   🛡️ Безопасное хранение паролей с использованием хэширования (bcrypt).
    *   🔑 Система авторизации на основе JWT-токенов (стандарт OAuth2).
*   **Управление контентом:**
    *   ✍️ CRUD-операции с ссылками, возможность создания короткой ссылки, редирект на основную при нажатии на короткую.  
    *   📈 Подсчет нажатий на короткую ссылку и выведение количества нажатий пользователю.
*   **Telegram-бот как клиент:**
    *   🔑 Управление аккаунтом с помощью кнопок (регистрация и авторизация).
    *   🤖 Интерактивные inline-кнопки для изменения и удаления ссылок.
    *   💬 Удобная навигация с помощью постоянной Reply-клавиатуры.
    *   🧠 Использование машины состояний (FSM) для реализации пошаговых диалогов.
*   **API:**
    *   📄 Автоматически генерируемая интерактивная документация (Swagger UI, ReDoc).
*   **Docker:**
    *   🐋 Сборка приложения с помощью Docker и возможность запустить все приложение нажатием на одну кнопку.
*   **Pytest:**
    *   🧪 Тесты для эндроинтов приложения, которые отвечают за безопасность и управление данными.
*   **Alembic:**
    *   🔄 Миграции для PostgreSQL базы данных, обеспечивающие сохранение данных при изменении самой базы данных.

---

## 🏁 Начало работы (Запуск через Docker)

### Требования
*   Python 3.10+
*   Docker
*   Токен Telegram-бота от [@BotFather](https://t.me/BotFather)

### Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Varenik-vkusny/Link-simplifier.git
    cd Link-simplifier
    ```

2.  **Создайте файл .env**
    *   Создайте файл .env в корневой папке проекта на основе .env.example
    *   Вставьте в переменную BOT_TOKEN токен бота с BotFather.
    *   Замените токен бота в .env и сгенерируйте свой собственный SECRET_KEY

3.  **Соберите и запустите приложение:**
    *   Соберите приложения и запустите его с помощью команды:
    ```bash
    docker-compose up --build -d
    ```

4.  **Примените миграции:**
    *   Примените миграции alembic с помощью команды:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
5.  **Готово! Ваше приложение запущено!**

*   API будет доступен по адресу http://localhost:8000.
*   Документация по адресу http://localhost:8000/docs.
*   Ваш бот уже запущен!

### Остановка приложения
   *   Остановить приложение можно по команде:
    ```bash
    docker-compose down
    ```
---
