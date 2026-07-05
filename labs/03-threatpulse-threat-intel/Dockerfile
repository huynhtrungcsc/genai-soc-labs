FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY backend ./backend
COPY frontend ./frontend
COPY scripts ./scripts
COPY sample-data ./sample-data

RUN python -m pip install --no-cache-dir -e .

EXPOSE 8003
CMD ["uvicorn", "app.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8003"]
