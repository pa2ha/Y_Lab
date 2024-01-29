# Используем базовый образ Python 3.10 slim
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей в контейнер и устанавливаем зависимости
COPY requirements.txt requirements.txt
COPY .env .env
RUN pip install --no-cache-dir -r requirements.txt
ENV DOTENV_PATH="/app/.env"
# Копируем все файлы из текущего каталога в рабочую директорию контейнера
COPY . .

CMD ["tail", "-f", "/dev/null"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
