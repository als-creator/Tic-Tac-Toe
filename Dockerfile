FROM python:3.12-slim

# Устанавливаем системные библиотеки для работы GUI (Tkinter и X11)
RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    && rm -rf /var/list/apt/lists/*

# Создаем рабочую папку в контейнере
WORKDIR /app

# Копируем файлы проекта (теперь копируем icon.ico вместо icon.png)
COPY main.py .
COPY icon.ico .

# Команда для запуска приложения внутри контейнера
CMD ["python", "main.py"]
LABEL org.opencontainers.image.source="https://github.com/als-creator/Tic-Tac-Toe"
