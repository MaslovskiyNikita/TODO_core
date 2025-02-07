FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости через Poetry
RUN poetry install --no-root

# Копируем остальную часть проекта
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1

# Запускаем скрипт entrypoint
ENTRYPOINT ["./entrypoint.sh"]