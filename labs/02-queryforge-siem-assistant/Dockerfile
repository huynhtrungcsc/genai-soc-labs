FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    QUERYFORGE_DATABASE_PATH=/app/data/queryforge.db

WORKDIR /app

COPY pyproject.toml README.md ./
COPY backend ./backend
COPY frontend ./frontend
COPY sample-data ./sample-data

RUN pip install --no-cache-dir .

EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8002"]
