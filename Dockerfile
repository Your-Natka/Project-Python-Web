# Використовуємо Python 3.12
FROM python:3.12-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли проекту
COPY ./app ./app
COPY requirements.txt ./requirements.txt

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# Команда запуску FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
