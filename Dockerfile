# Берем базовый образ с Python
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем файлы


# Устанавливаем зависимости
RUN apt-get update && apt-get install -y p7zip-full && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN 7z x val.7z


# Запуск (вариант 1: последовательно)
CMD ["sh", "-c", "python media_service.py & python test_script.py"]
