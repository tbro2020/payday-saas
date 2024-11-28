#!/bin/bash

# Wait for the master to be ready
until pg_isready -h master -p 5432 -U replicator; do
  echo "Waiting for master to be ready..."
  sleep 2
done

# Sync data from master
PGDATA="/var/lib/postgresql/data"
rm -rf ${PGDATA}/*
pg_basebackup -h master -D ${PGDATA} -U replicator -Fp -Xs -R

# Start PostgreSQL
exec postgres