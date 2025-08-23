[Читать на русском](README_RU.md)
---

# ✒️ Link Simplifier: A High-Performance URL Shortener Service

[![Run Python Tests](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml/badge.svg)](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml)

An asynchronous web application built with FastAPI, featuring a hybrid storage architecture (PostgreSQL + Redis) to ensure instantaneous redirects. A Telegram bot built with Aiogram 3 serves as the client interface.

---

## 🚀 Architecture & Technology

This project demonstrates the development of a high-performance and resilient web service using modern backend engineering practices.

*   **FastAPI API:** An asynchronous REST API for managing users and links.
*   **Hybrid Storage:**
    *   **PostgreSQL:** Serves as the reliable, long-term "Source of Truth" for user data and complete link information.
    *   **Redis:** Acts as the primary **operational data store** for "short_code -> original_url" pairs, enabling redirects in microseconds. It is also used for **atomic click counting** and **caching** user link lists.
*   **Background Task (APScheduler):** Periodically synchronizes click counts from Redis to the main PostgreSQL database.
*   **Aiogram 3 Telegram Bot:** A full-featured client for interacting with the API.

### 🛠️ Tech Stack

*   **Backend:** Python 3.12, **FastAPI**, **SQLAlchemy 2.0 (async)**, Pydantic V2, Alembic
*   **Databases:** **PostgreSQL**, **Redis**
*   **Authentication:** **JWT** (python-jose), **OAuth2**, passlib[bcrypt]
*   **Infrastructure & DevOps:** **Docker**, **Docker Compose**, **CI/CD (GitHub Actions)**
*   **Testing:** **Pytest**, pytest-mock, httpx

---

## ✨ Key Features

*   **High Performance:**
    *   **Redis-First Architecture for Redirects:** Redirect requests are handled directly by Redis without touching the primary database, ensuring minimal latency.
    *   **Asynchronous Click Counting:** Utilizes Redis's atomic `INCR` operation to prevent blocking the main thread.
    *   **API Response Caching:** User link lists are cached to reduce the load on PostgreSQL.
*   **Reliability & Code Quality:**
    *   **Comprehensive Test Coverage:** E2E tests for all API endpoints and Unit tests for business logic, including dependency mocking.
    *   **Isolated Test Environment:** Pytest is configured to work with an in-memory SQLite database and a separate test Redis database.
    *   **Automated Quality Assurance:** A CI pipeline on GitHub Actions runs tests on every commit.
    *   **Secure Authentication:** Implementation of the OAuth2 standard with JWTs to protect endpoints.
*   **Thoughtful Architecture:**
    *   **Resource Management via `lifespan`:** Proper initialization and closing of the Redis connection pool.
    *   **Cache Invalidation:** Automatic clearing of a user's cache upon link creation, update, or deletion.
    *   **DB Migrations:** Safe PostgreSQL schema management with Alembic.

---

## 🏁 Getting Started

### Prerequisites
*   Docker
*   Docker Compose

### Installation & Launch

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Varenik-vkusny/Link-simplifier.git
    cd Link-simplifier
    ```

2.  **Set up environment variables:**
    *   Copy `.env.example` to `.env`.
    *   Fill in `BOT_TOKEN`, `SECRET_KEY`, and other required variables.

3.  **Run the application:**
    ```bash
    docker-compose up --build
    ```

4.  **Apply migrations (in a separate terminal):**
    *   Wait for the containers to start up, then execute:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
5.  **Done!**
    *   The API is available at `http://localhost:8000`
    *   Interactive API documentation: `http://localhost:8000/docs`
    *   Your Telegram bot is now running and ready to use.

---

### Running Tests

A running Redis container is required to run the E2E tests.

1.  **Start Redis in detached mode:**
    ```bash
    docker-compose up -d redis
    ```
2.  **Install dependencies and run tests:**
    ```bash
    # (Activate your virtual environment)
    pip install -r requirements.txt
    pytest
    ```
3.  **Stop Redis after testing:**
    ```bash
    docker-compose down
    ```

---
### Stopping the Application
```bash
docker-compose down
