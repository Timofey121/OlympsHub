FROM python:3.10
WORKDIR /app
COPY ../../weqdefw/TelegramBot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ../../weqdefw/TelegramBot .
CMD ["python", "bot.py"]