# ✒️ Link Simplifier

[![Run Python Tests](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml/badge.svg)](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml)

A modern web application for URL shortening, featuring a backend built with the high-performance FastAPI framework and a user-friendly Telegram bot client powered by aiogram 3.

---

## 🚀 About The Project

This project is a convenient tool for creating short URLs. It consists of two main parts:

*   **FastAPI REST API:** A high-speed backend that handles all business logic, manages data in a PostgreSQL database, and ensures secure JWT-based authentication.
*   **Telegram Bot (aiogram 3):** An interactive and friendly client for interacting with the service through the familiar Telegram interface.

This project showcases a full cycle of modern backend development: from API design and database management to testing, migration setup, and containerization with Docker.

---

## 🛠️ Tech Stack

*   **Backend:**
    *   ![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)
    *   ![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-009688?style=for-the-badge&logo=fastapi)
    *   ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-DB4437?style=for-the-badge&logo=sqlalchemy)
    *   ![Pydantic](https://img.shields.io/badge/Pydantic-v2-E96F00?style=for-the-badge)
*   **Telegram Bot:**
    *   ![aiogram](https://img.shields.io/badge/aiogram-3.x-26A5E4?style=for-the-badge)
    *   ![httpx](https://img.shields.io/badge/httpx-async-000000?style=for-the-badge)
*   **Database & Migrations:**
    *   ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)
    *   ![Alembic](https://img.shields.io/badge/Alembic-migrations-4E2A84?style=for-the-badge)
*   **Authentication & Tooling:**
    *   `python-jose` (JWT Tokens)
    *   `passlib` & `bcrypt` (Password Hashing)
    *   `Uvicorn` (ASGI Server)
    *   `python-dotenv` (Environment Variables)
*   **Containerization & Testing:**
    *   ![Docker](https://img.shields.io/badge/Docker-compose-2496ED?style=for-the-badge&logo=docker)
    *   ![Pytest](https://img.shields.io/badge/Pytest-testing-0A9EDC?style=for-the-badge&logo=pytest)

---

## ✨ Key Features

*   **Authentication & Authorization:**
    *   🔐 User registration and login via username/password.
    *   🛡️ Secure password storage using hashing (bcrypt).
    *   🔑 JWT-based authentication system (OAuth2 standard).
*   **Link Management:**
    *   ✍️ Full CRUD operations for links (Create, Read, Update, Delete).
    *   🔄 Automatic redirection from short links to the original URL.
    *   📈 Tracking of click counts for each link.
*   **Telegram Bot as a Client:**
    *   🔑 Account management (registration, login) via interactive buttons.
    *   🤖 Intuitive link management using inline keyboard buttons.
    *   💬 Easy navigation with a persistent Reply Keyboard.
    *   🧠 Finite State Machine (FSM) for handling multi-step user dialogues.
*   **Code Quality & Infrastructure:**
    *   📄 Automatically generated interactive API documentation (Swagger UI, ReDoc).
    *   🐋 The entire application and its database are containerized with Docker.
    *   🧪 Integration tests for critical API endpoints covering security and data management.
    *   🔄 Database schema versioning managed by Alembic migrations.

---

## 🏁 Getting Started (via Docker)

This is the recommended and easiest way to run the project.

### Prerequisites
*   [Docker](https://www.docker.com/products/docker-desktop/) installed.
*   A Telegram Bot Token from [@BotFather](https://t.me/BotFather).

### Installation and Launch

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Varenik-vkusny/Link-simplifier.git
    cd Link-simplifier
    ```

2.  **Create the `.env` file:**
    *   Create a copy of the `.env.example` file and name it `.env`.
    *   Open the new `.env` file and paste your Telegram Bot Token into the `BOT_TOKEN` variable.
    *   (Optional) You can also generate your own `SECRET_KEY` for added security.

3.  **Build and run the containers:**
    Execute a single command to build the image and start all services:
    ```bash
    docker-compose up --build -d
    ```
    *   `--build`: Forces a rebuild of the image if there are changes in your code.
    *   `-d`: Runs the containers in detached (background) mode.

4.  **Apply the database migrations:**
    Once the containers are running, execute this command to create the necessary tables in the database:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
    *   `docker-compose exec web`: Executes a command inside the running `web` container.
    *   `alembic upgrade head`: Applies the latest database migrations.

5.  **Done! Your application is now running!**

*   The API is available at `http://localhost:8000`.
*   Interactive API documentation is at `http://localhost:8000/docs`.
*   Your Telegram bot is up and ready to use!

### Stopping the application
To stop all running containers, use the following command:
```bash
docker-compose down
