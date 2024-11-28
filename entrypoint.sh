#!/bin/bash

set -e

log() {
  echo "[$(date)] $1"
}

# Master node setup
if [ "$POSTGRES_REPLICATION_ROLE" == "master" ]; then
  log "Configuring master node..."
  echo "host replication all all md5" >> "$PGDATA/pg_hba.conf"
  echo "host all all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
  echo "listen_addresses = '*'" >> "$PGDATA/postgresql.conf"
  echo "wal_level = replica" >> "$PGDATA/postgresql.conf"
  echo "max_wal_senders = 5" >> "$PGDATA/postgresql.conf"
  echo "wal_keep_size = 64" >> "$PGDATA/postgresql.conf"
  echo "archive_mode = on" >> "$PGDATA/postgresql.conf"
  # Create replication user
  psql -U postgres -c "CREATE USER replica WITH REPLICATION PASSWORD 'password';"
  log "Master node configured."
fi

# Start PostgreSQL service
log "Starting PostgreSQL service..."
docker-entrypoint.sh postgres &

# Slave node setup
if [ "$POSTGRES_REPLICATION_ROLE" == "replica" ]; then
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
fi

exec "$@"