#!/bin/bash

set -e

log() {
  echo "[$(date)] $1"
}

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

# Start PostgreSQL service
log "Starting PostgreSQL service..."
exec docker-entrypoint.sh postgres