FROM python:3.14-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

RUN uv sync --no-dev

RUN mkdir -p /app/logs

CMD ["uv", "run", "--no-sync", "python", "src/proyecto_ingenieria_dato/LosCaballas_migraña.py"]