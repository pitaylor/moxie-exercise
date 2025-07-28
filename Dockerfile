FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
