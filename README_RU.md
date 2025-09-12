[Read in English](README.md)
---

# ✒️ Link Simplifier: Высокопроизводительный сервис сокращения ссылок

[![Run Python Tests](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml/badge.svg)](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml)

Асинхронное веб-приложение на FastAPI c гибридной архитектурой хранения данных (PostgreSQL + Redis) для обеспечения мгновенного редиректа. В качестве клиентского интерфейса выступает Telegram-бот. Проект полностью контейнеризирован и готов к развертыванию в Kubernetes.

---

## 🚀 Архитектура и технологии

Проект демонстрирует построение высокопроизводительного и отказоустойчивого веб-сервиса с использованием современных практик бэкенд-разработки.

*   **API на FastAPI:** Асинхронный REST API для управления пользователями и ссылками.
*   **Гибридное хранилище:**
    *   **PostgreSQL:** Используется как надежное, долгосрочное хранилище ("Source of Truth") для данных о пользователях и полной информации о ссылках.
    *   **Redis:** Выступает в роли основного **оперативного хранилища** для пар "короткий код -> оригинальная ссылка", обеспечивая редирект за микросекунды. Также используется для **атомарного подсчета кликов** и **кэширования** списков ссылок.
*   **Фоновая задача (APScheduler):** Периодически синхронизирует счетчики кликов из Redis с основной базой данных PostgreSQL.
*   **Telegram-бот на Aiogram 3:** Полнофункциональный клиент для взаимодействия с API.

### 🛠️ Стек 

*   **Бэкенд:** Python 3.12, **FastAPI**, **SQLAlchemy 2.0 (async)**, Pydantic V2, Alembic
*   **Базы данных:** **PostgreSQL**, **Redis**
*   **Аутентификация:** **JWT** (python-jose), **OAuth2**, passlib[bcrypt]
*   **Инфраструктура и DevOps:** **Docker**, **Docker Compose**, **Kubernetes (K8s)**, **CI/CD (GitHub Actions)**
*   **Тестирование:** **Pytest**, pytest-mock, httpx

---

## ✨ Ключевые возможности

*   **Высокая производительность:**
    *   **Redis-First архитектура для редиректов:** Запросы на редирект обрабатываются напрямую из Redis, не затрагивая основную базу данных, что обеспечивает минимальную задержку.
    *   **Асинхронный подсчет кликов:** Используется атомарная операция `INCR` в Redis, чтобы не блокировать основной поток.
    *   **Кэширование API-ответов:** Списки ссылок пользователя кэшируются для снижения нагрузки на PostgreSQL.
*   **Надежность и качество кода:**
    *   **Полное покрытие тестами:** E2E-тесты для всех эндпоинтов и Unit-тесты для бизнес-логики кэширования с подменой зависимостей (`dependency_overrides`).
    *   **Изолированное тестовое окружение:** Настройка `pytest` для работы с in-memory SQLite и тестовой базой Redis.
    *   **Автоматизированная проверка качества:** CI-пайплайн на GitHub Actions запускает тесты при каждом коммите.
*   **Продуманная архитектура:**
    *   **Управление ресурсами через `lifespan`:** Корректная инициализация и закрытие пула соединений Redis.
    *   **Инвалидация кэша:** Автоматическая очистка кэша пользователя при создании, изменении или удалении ссылок.
    *   **Миграции БД:** Управление схемой PostgreSQL с помощью Alembic.

---

## 🏁 Запуск и Развертывание

### С помощью Docker Compose (для локальной разработки)

#### Требования
*   Docker
*   Docker Compose

#### Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Varenik-vkusny/Link-simplifier.git
    cd Link-simplifier
    ```

2.  **Настройте переменные окружения:**
    *   Скопируйте `.env.example` в `.env` и `.env.db.example` в `.env.db`.
    *   Заполните `BOT_TOKEN`, `SECRET_KEY` и другие необходимые переменные.

3.  **Запустите приложение:**
    ```bash
    docker-compose up --build
    ```

4.  **Примените миграции (в отдельном терминале):**
    *   Дождитесь, пока контейнеры запустятся, и выполните:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
5.  **Готово!**
    *   API доступен по адресу `http://localhost:8000`
    *   Интерактивная документация API: `http://localhost:8000/docs`
    *   Ваш Telegram-бот запущен и готов к работе.

#### Остановка приложения
```bash
docker-compose down
```
---

### В Kubernetes (для продакшн-подобного окружения)

Этот раздел описывает, как развернуть приложение в локальном кластере Kubernetes, например, в Minikube.

#### Предварительные требования

1.  **kubectl**: Установленный и настроенный клиент командной строки Kubernetes.
2.  **Minikube**: Установленный локальный кластер Kubernetes.
3.  **Nginx Ingress Controller**: Установленный в Minikube. Включается командой:
    ```bash
    minikube addons enable ingress
    ```

#### 1. Настройка секретов

Все чувствительные данные должны быть созданы внутри кластера Kubernetes. Выполните следующую команду, чтобы создать секрет `app-secrets`. **Замените значения `SECRET_KEY` и `BOT_TOKEN` на свои.**

```bash
kubectl create secret generic app-secrets --namespace=link-simplifier \
  --from-literal=DB_USER='Short' \
  --from-literal=DB_PASSWORD='Link' \
  --from-literal=SECRET_KEY='YOUR_OWN_SECRET_KEY_HERE' \
  --from-literal=BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN_HERE'
```

#### 2. Применение манифестов

1.  **Создайте Namespace:**
    ```bash
    kubectl apply -f k8s/00-namespace.yaml
    ```
    
2.  **Примените все остальные манифесты** одной командой. `migration-job` автоматически применит миграции.
    ```bash
    kubectl apply -f k8s/
    ```

#### 3. Проверка статуса развертывания
```bash
kubectl get all --namespace=link-simplifier
```
Вы должны увидеть запущенные поды для `api`, `bot`, `postgres` и `redis`. Убедитесь, что джоба миграции `migration-job` имеет статус `Completed`.

#### 4. Доступ к приложению

1.  **Получите прямой URL для доступа к Ingress-контроллеру:**
    ```bash
    minikube service ingress-nginx-controller -n ingress-nginx --url
    ```
    Команда выведет URL, например `http://127.0.0.1:57135`. **Скопируйте его**.

2.  **Проверьте API с помощью `curl`:**
    Отправьте запрос, используя полученный URL и заголовок `-H "Host: links.local"`.
    ```bash
    # Замените http://127.0.0.1:XXXXX на URL из предыдущего шага
    curl -v -H "Host: links.local" http://127.0.0.1:XXXXX/docs
    ```
    **Ожидаемый результат:** Ответ `HTTP/1.1 200 OK` и HTML-код документации.

#### 5. Проверка и отладка

1.  **Проверьте Ingress Controller:**
    ```bash
    kubectl get pods -n ingress-nginx
    ```
    *   **Ожидаемый результат:** Pod `ingress-nginx-controller-...` должен быть в статусе `Running`.

2.  **Проверьте ваш Ingress ресурс:**
    ```bash
    kubectl describe ingress ingress -n link-simplifier
    ```
    *   **Что искать:** `Host` должен быть `links.local`, а в секции `Backends` должны быть IP-адреса подов вашего `api-service`.

#### 6. Очистка

Чтобы удалить все созданные в Kubernetes ресурсы, просто удалите `namespace`:
```bash
kubectl delete namespace link-simplifier
```

---
### Запуск тестов

1.  **Запустите Redis в фоновом режиме:**
    ```bash
    docker-compose up -d redis
    ```
2.  **Установите зависимости и запустите тесты:**
    ```bash
    pip install -r requirements.txt
    pytest
    ```
3.  **Остановите Redis после тестов:**
    ```bash
    docker-compose down
