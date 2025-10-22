# Multi-stage Docker build for OlympiadHub Django Application
# Stage 1: Builder stage for dependency compilation
FROM python:3.11 as builder

WORKDIR /usr/src/app

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnss3-tools \
    libnspr4 \
    wget \
    unzip \
    gnupg2 \
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
    libgbm1 \
    chromium

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# Stage 2: Final production image
FROM python:3.11

# Create directories and user for security
RUN mkdir -p /home/app/web/staticfiles /home/app/web/mediafiles && \
    groupadd app && \
    useradd -m -g app app -p PASSWORD

# Set environment variables
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

# Install system dependencies and Chromium in final image
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
    libgbm1 \
    chromium

# Copy dependencies from builder stage
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application files
COPY entrypoint.prod.sh $APP_HOME
COPY . $APP_HOME

# Set proper permissions
RUN chown -R app:app $APP_HOME && chmod -R 777 /home/app

# Set environment variables for ChromeDriver and display
ENV WDM_LOCAL=/usr/local/bin
ENV PATH="/usr/bin:${PATH}"
ENV DISPLAY=:99

# Switch to non-root user for security
USER app

# Create cache directory for ChromeDriver
RUN mkdir -p /home/app/.wdm/drivers && chown -R app:app /home/app/.wdm

# Make entrypoint script executable
RUN chmod +x entrypoint.prod.sh

# Set entrypoint
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]