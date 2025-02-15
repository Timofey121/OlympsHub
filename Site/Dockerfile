FROM python:3.11 as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies AND Chrome in the final image
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

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.11

# Create directories and user
RUN mkdir -p /home/app/web/staticfiles /home/app/web/mediafiles && \
    groupadd app && \
    useradd -m -g app app -p PASSWORD

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

# Install netcat and copy dependencies
RUN apt-get update && \
    apt-get install -y netcat-traditional xvfb

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application files
COPY entrypoint.prod.sh $APP_HOME
COPY . $APP_HOME

# Set permissions
RUN chown -R app:app $APP_HOME

RUN chmod -R 777 /home/app
ENV WDM_LOCAL=/usr/local/bin
ENV PATH="/usr/bin:${PATH}"

# Set the DISPLAY environment variable
ENV DISPLAY=:99

# Switch to the app user
USER app

# Set permissions for ChromeDriver cache
RUN mkdir -p /home/app/.wdm/drivers \
    && chown -R app:app /home/app/.wdm

# Make entrypoint script executable
RUN chmod +x entrypoint.prod.sh

# Set the entrypoint
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]