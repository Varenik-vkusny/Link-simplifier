[Read in Russian](README.ru.md)
---

# ✒️ Link Simplifier: A High-Performance URL Shortening Service

[![Run Python Tests](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml/badge.svg)](https://github.com/Varenik-vkusny/Link-simplifier/actions/workflows/ci.yml)

An asynchronous web application built with FastAPI, featuring a hybrid data storage architecture (PostgreSQL + Redis) to ensure instant redirects. A Telegram bot serves as the client interface. The project is fully containerized and ready for deployment in Kubernetes.

---

## 🚀 Architecture and Technologies

The project demonstrates how to build a high-performance and fault-tolerant web service using modern backend development practices.

*   **API with FastAPI:** An asynchronous REST API for managing users and links.
*   **Hybrid Storage:**
    *   **PostgreSQL:** Used as a reliable, long-term "Source of Truth" for user data and complete link information.
    *   **Redis:** Acts as the primary **operational data store** for "short code -> original URL" pairs, enabling redirects in microseconds. It is also used for **atomic click counting** and **caching** link lists.
*   **Background Task (APScheduler):** Periodically synchronizes click counts from Redis to the main PostgreSQL database.
*   **Telegram Bot with Aiogram 3:** A full-featured client for interacting with the API.

### 🛠️ Tech Stack 

*   **Backend:** Python 3.12, **FastAPI**, **SQLAlchemy 2.0 (async)**, Pydantic V2, Alembic
*   **Databases:** **PostgreSQL**, **Redis**
*   **Authentication:** **JWT** (python-jose), **OAuth2**, passlib[bcrypt]
*   **Infrastructure & DevOps:** **Docker**, **Docker Compose**, **Kubernetes (K8s)**, **CI/CD (GitHub Actions)**
*   **Testing:** **Pytest**, pytest-mock, httpx

---

## ✨ Key Features

*   **High Performance:**
    *   **Redis-First Architecture for Redirects:** Redirect requests are handled directly from Redis without touching the main database, ensuring minimal latency.
    *   **Asynchronous Click Counting:** Uses the atomic `INCR` operation in Redis to avoid blocking the main thread.
    *   **API Response Caching:** User link lists are cached to reduce the load on PostgreSQL.
*   **Reliability and Code Quality:**
    *   **Full Test Coverage:** E2E tests for all endpoints and unit tests for caching logic using dependency overrides.
    *   **Isolated Test Environment:** Pytest is configured to work with an in-memory SQLite and a test Redis database.
    *   **Automated Quality Assurance:** A CI pipeline on GitHub Actions runs tests on every commit.
*   **Thoughtful Architecture:**
    *   **Resource Management via `lifespan`:** Correct initialization and closing of the Redis connection pool.
    *   **Cache Invalidation:** The user's cache is automatically cleared when links are created, updated, or deleted.
    *   **DB Migrations:** Safe PostgreSQL schema management with Alembic.

---

## 🏁 Launch and Deployment

### Using Docker Compose (for local development)

#### Prerequisites
*   Docker
*   Docker Compose

#### Installation and Startup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Varenik-vkusny/Link-simplifier.git
    cd Link-simplifier
    ```

2.  **Set up environment variables:**
    *   Copy `.env.example` to `.env` and `.env.db.example` to `.env.db`.
    *   Fill in `BOT_TOKEN`, `SECRET_KEY`, and other required variables.

3.  **Run the application:**
    ```bash
    docker-compose up --build
    ```

4.  **Apply migrations (in a separate terminal):**
    *   Wait for the containers to start, then run:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
5.  **Done!**
    *   The API is available at `http://localhost:8000`
    *   Interactive API documentation: `http://localhost:8000/docs`
    *   Your Telegram bot is running and ready to use.

#### Stopping the Application
```bash
docker-compose down
```
---

### In Kubernetes (for a production-like environment)

This section describes how to deploy the application in a local Kubernetes cluster, such as Minikube.

#### Prerequisites

1.  **kubectl**: An installed and configured Kubernetes command-line client.
2.  **Minikube**: An installed local Kubernetes cluster.
3.  **Nginx Ingress Controller**: Installed in Minikube. It can be enabled with the command:
    ```bash
    minikube addons enable ingress
    ```

#### 1. Secret Configuration

All sensitive data must be created within the Kubernetes cluster. Run the following command to create the `app-secrets` secret. **Replace the `SECRET_KEY` and `BOT_TOKEN` values with your own.**

```bash
kubectl create secret generic app-secrets --namespace=link-simplifier \
  --from-literal=DB_USER='Short' \
  --from-literal=DB_PASSWORD='Link' \
  --from-literal=SECRET_KEY='YOUR_OWN_SECRET_KEY_HERE' \
  --from-literal=BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN_HERE'
```

#### 2. Applying the Manifests

1.  **Create the Namespace:**
    ```bash
    kubectl apply -f k8s/00-namespace.yaml
    ```
    
2.  **Apply all other manifests** with a single command. The `migration-job` will automatically apply migrations.
    ```bash
    kubectl apply -f k8s/
    ```

#### 3. Checking Deployment Status
```bash
kubectl get all --namespace=link-simplifier
```
You should see running pods for `api`, `bot`, `postgres`, and `redis`. Ensure that the `migration-job` has a `Completed` status.

#### 4. Accessing the Application

1.  **Get the direct access URL for the Ingress controller:**
    ```bash
    minikube service ingress-nginx-controller -n ingress-nginx --url
    ```
    The command will output a URL, for example, `http://127.0.0.1:57135`. **Copy it**.

2.  **Test the API using `curl`:**
    Send a request using the obtained URL and the `-H "Host: links.local"` header.
    ```bash
    # Replace http://127.0.0.1:XXXXX with the URL from the previous step
    curl -v -H "Host: links.local" http://127.0.0.1:XXXXX/docs
    ```
    **Expected result:** An `HTTP/1.1 200 OK` response and the documentation HTML.

#### 5. Verification and Debugging

1.  **Check the Ingress Controller:**
    ```bash
    kubectl get pods -n ingress-nginx
    ```
    *   **Expected result:** The `ingress-nginx-controller-...` pod should be in the `Running` status.

2.  **Check your Ingress resource:**
    ```bash
    kubectl describe ingress ingress -n link-simplifier
    ```
    *   **What to look for:** The `Host` should be `links.local`, and the `Backends` section should contain the IP addresses of your `api-service` pods.

#### 6. Cleanup

To delete all the Kubernetes resources created, simply delete the namespace:
```bash
kubectl delete namespace link-simplifier
```

---
### Running Tests

1.  **Start Redis in the background:**
    ```bash
    docker-compose up -d redis
    ```
2.  **Install dependencies and run tests:**
    ```bash
    pip install -r requirements.txt
    pytest
    ```
3.  **Stop Redis after the tests:**
    ```bash
    docker-compose down
