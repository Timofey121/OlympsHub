FROM python:3.11 as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnss3-tools \
    libnspr4 \
    wget \
    gnupg2 \
    unzip \
    netcat-traditional \
    xvfb \
    libgconf-2-4 \
    libxi6 \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libasound2 \
    libxrandr2 \
    libatk1.0-0 \
    libgtk-3-0 \
    libxss1 \
    libgbm1

# Установка Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Обновление pip и установка Python-зависимостей
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.11

# Создание директорий и пользователя
RUN mkdir -p /home/app/web/staticfiles /home/app/web/mediafiles && \
    groupadd app && \
    useradd -m -g app app -p PASSWORD

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

# Установка системных зависимостей и Google Chrome в финальном образе
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    xvfb \
    libnss3 \
    libnss3-tools \
    libnspr4 \
    libgconf-2-4 \
    libxi6 \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libasound2 \
    libxrandr2 \
    libatk1.0-0 \
    libgtk-3-0 \
    libxss1 \
    libgbm1

# Установка Google Chrome в финальном образе
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Копирование зависимостей из builder-стадии
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копирование файлов приложения
COPY entrypoint.prod.sh $APP_HOME
COPY . $APP_HOME

# Установка прав
RUN chown -R app:app $APP_HOME

RUN chmod -R 777 /home/app
ENV WDM_LOCAL=/usr/local/bin
ENV PATH="/usr/bin:${PATH}"

# Установка переменной окружения DISPLAY
ENV DISPLAY=:99

# Переключение на пользователя app
USER app

# Установка прав для кэша ChromeDriver
RUN mkdir -p /home/app/.wdm/drivers \
    && chown -R app:app /home/app/.wdm

# Сделать entrypoint-скрипт исполняемым
RUN chmod +x entrypoint.prod.sh

# Установка entrypoint
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]