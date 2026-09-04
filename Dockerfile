FROM python:3.12-slim

# Устанавливаем системные библиотеки для работы GUI (Tkinter и X11)
RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую папку в контейнере
WORKDIR /app

# Копируем файлы проекта (иконка окна — PNG; PhotoImage не читает ICO)
COPY main.py .
COPY icon.png .

# Команда для запуска приложения внутри контейнера
CMD ["python", "main.py"]
LABEL org.opencontainers.image.source="https://github.com/als-creator/Tic-Tac-Toe"
