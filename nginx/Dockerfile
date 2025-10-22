# OlympiadHub Nginx Docker Image
FROM nginx:1.25-alpine

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/

# Create necessary directories
RUN mkdir -p /home/app/web/staticfiles /home/app/web/mediafiles

# Expose ports
EXPOSE 80 443