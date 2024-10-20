FROM python:3.12-slim

WORKDIR /backend

RUN pip install --upgrade pip
ENV PATH="/root/.local/bin:$PATH"
# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
RUN pip install poetry
COPY . .

RUN chmod +x ./scripts/entrypoint.sh ./scripts/wait-for-it.sh
EXPOSE 8000
