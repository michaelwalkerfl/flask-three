#!/bin/sh
set -e

wait_for() {
    echo "Waiting for $1 at $2:$3..."
    until nc -z "$2" "$3"; do
        sleep 0.5
    done
    echo "$1 is up."
}

[ -n "$DB_HOST" ] && wait_for PostgreSQL "$DB_HOST" "${DB_PORT:-5432}"
[ -n "$REDIS_HOST" ] && wait_for Redis "$REDIS_HOST" "${REDIS_PORT:-6379}"

# Idempotent setup: creates missing tables, roles and the admin user. Never drops data.
if [ "${RUN_SETUP:-1}" = "1" ]; then
    flask create-database
    flask create-roles
    flask create-admin
fi

exec "$@"
