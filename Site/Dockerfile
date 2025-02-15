FROM python:3.11 as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновляем систему и устанавливаем зависимости
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y postgresql gcc python3-dev musl-dev wget gnupg2 unzip netcat-traditional nginx gunicorn xvfb \

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y postgresql gcc python3-dev musl-dev wget gnupg2 unzip netcat-traditional nginx gunicorn xvfb libnss3


# Установка Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.11

# Создаем директории и пользователя
RUN mkdir -p /home/app/web/staticfiles /home/app/web/mediafiles && \
    groupadd app && \
    useradd -m -g app app -p PASSWORD

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

# Устанавливаем netcat и копируем зависимости
RUN apt-get update && \
    apt-get install -y netcat-traditional

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем файлы приложения, включая chromedriver
COPY entrypoint.prod.sh $APP_HOME
COPY . $APP_HOME

# Меняем владельца файлов и директории
RUN chown -R app:app $APP_HOME
RUN chmod +x /home/app/web/chromedriver

RUN chmod -R 777 /home/app
ENV WDM_LOCAL=/usr/local/bin

# Переходим к пользователю app
USER app

# Разрешаем выполнение entrypoint скрипта
RUN chmod +x entrypoint.prod.sh

# Определяем точку входа
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]