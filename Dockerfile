FROM python:3.14-slim

#Get uv from the official binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

#Install dependencies
RUN uv sync --frozen --no-install-project

COPY main.py ./
COPY static/ ./static/
COPY templates/ ./templates/

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
