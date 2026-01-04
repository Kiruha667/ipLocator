# 1. Берем легкий образ Python
FROM python:3.9-slim

# 2. Создаем папку внутри контейнера
WORKDIR /app

# 3. Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем твой код (main.py) внутрь контейнера
COPY main.py .

# 5. Команда для запуска (Важно: host 0.0.0.0 открывает доступ снаружи)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]