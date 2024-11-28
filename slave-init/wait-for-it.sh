#!/bin/bash

host=${MASTER_HOST:-"master"}
port=${MASTER_PORT:-5432}

echo "Checking for database at $host:$port..."

until pg_isready -h "$host" -p "$port" -U payday; do
  echo "Waiting for database $host:$port to be ready..."
  sleep 2
done

echo "Database $host:$port is ready."