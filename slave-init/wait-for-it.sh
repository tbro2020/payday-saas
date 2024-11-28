#!/bin/bash
# wait-for-it.sh

host=$1
shift
until pg_isready -h $host -U payday; do
  echo "Waiting for database $host to be ready..."
  sleep 2
done
echo "$host is ready"