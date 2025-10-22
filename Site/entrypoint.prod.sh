#!/bin/sh

# OlympiadHub Django Application Entrypoint Script
# This script ensures PostgreSQL is ready before starting the Django application

# Check if we're using PostgreSQL as the database
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL database to be ready..."

    # Wait for PostgreSQL to be available on the specified host and port
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL database is now available"
fi

# Execute the command passed to the container
exec "$@"