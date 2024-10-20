# URL Shortener

## A simple URL shortening service built using FastAPI, Celery, Redis, PostgreSQL, and Docker. This project provides an API to shorten long URLs, stores them in a database, and allows users to retrieve the original URL via the shortened URL.

### Requirements

- Docker (with Compose)

### Services

#### This project contains the following services:

- backend: The FastAPI backend API.
- celery_worker: Celery worker for processing asynchronous tasks.
- redis: Redis instance as a message broker.
- db: PostgreSQL database.
- frontend: Simple UI to test the URL Shortener.

### How to Run the Project

#### Clone the repository:

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

#### Build and run the services using Docker Compose:

```bash
    docker-compose up --build
```

### Access the services:

-        API: http://localhost:8000/docs
-        API (Swagger documentation): http://localhost:8000/docs
-        Frontend: http://localhost:3000 (URL shortening form)

### Using Frontend
1. To access frontend start service with docker as stated above.
2. The frontend is available at http://localhost:3000
3. Pass your URL to form and click Shorten
4. If URL was entered before you will see the shortened link below form.
5. If this is the first time that URL is passed into Shortener, there might appear message that URL is processed. After few seconds try to click once again on the Shorten button (having the same URL in the form) and the shortened version should appear below.

## Troubleshooting
1. When running on Windows bash scripts may be saved in CRLF mode what makes them unusable for docker. Happily it can be easily changed eg. using VS Code.
