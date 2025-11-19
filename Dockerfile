# Используем легкий образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код (это нужно для сборки, но docker-compose перекроет это volume-ом)
COPY . .

# Открываем порт 5000
EXPOSE 5000

# Команда запуска. --debug включает "вотчер" (автоперезагрузку)
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]