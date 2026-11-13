FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY cron_pipeline /etc/cron.d/cron_pipeline

RUN uv sync --no-dev

RUN mkdir -p /app/logs

COPY dump_env.sh /dump_env.sh

# Give execute permissions
RUN chmod +x /dump_env.sh && chmod 0644 /etc/cron.d/cron_pipeline

CMD ["/dump_env.sh"]