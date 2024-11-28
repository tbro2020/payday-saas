#!/bin/bash

set -e

log() {
  echo "[$(date)] $1"
}

log "Configuring replica node..."
until pg_isready -h master -p 5432 -U postgres; do
  log "Waiting for master to be ready..."
  sleep 2
done
log "Master is ready. Starting base backup..."
rm -rf $PGDATA/*
pg_basebackup -h master -D $PGDATA -U replica -v -P -W
echo "standby_mode = 'on'" >> "$PGDATA/recovery.conf"
echo "primary_conninfo = 'host=master port=5432 user=replica password=password'" >> "$PGDATA/recovery.conf"
log "Replica node configured."

# Start PostgreSQL service
log "Starting PostgreSQL service..."
exec docker-entrypoint.sh postgres
