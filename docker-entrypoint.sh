#!/bin/sh

# wait for postgresql
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "PostgreSQL started"

# wait for redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
    sleep 0.1
done
echo "Redis started"

# initialize the database
echo "Initializing database..."
flask create-database
flask create-roles
flask create-admin

# start flask
echo "Starting Flask..."
exec flask run --host=0.0.0.0 --port=5001 