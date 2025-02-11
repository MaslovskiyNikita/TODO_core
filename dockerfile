FROM python:3.12-slim AS builder


RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install poetry


WORKDIR /app


COPY pyproject.toml poetry.lock ./


RUN poetry install --no-root


FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app


COPY --from=builder /root/.cache /root/.cache
COPY --from=builder /app /app


ENV PYTHONUNBUFFERED 1


COPY . .


ENTRYPOINT ["./entrypoint.sh"]