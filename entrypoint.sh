#!/bin/bash

set -e

# Master node setup
if [ "$POSTGRES_REPLICATION_ROLE" == "master" ]; then
  echo "Configuring master node..."
  echo "host replication all all md5" >> "$PGDATA/pg_hba.conf"
  echo "host all all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
  echo "listen_addresses = '*'" >> "$PGDATA/postgresql.conf"
  echo "wal_level = replica" >> "$PGDATA/postgresql.conf"
  echo "max_wal_senders = 5" >> "$PGDATA/postgresql.conf"
  echo "wal_keep_size = 64" >> "$PGDATA/postgresql.conf"
  echo "archive_mode = on" >> "$PGDATA/postgresql.conf"
  # Create replication user
  psql -U postgres -c "CREATE USER replica WITH REPLICATION PASSWORD 'password';"
fi

# Start PostgreSQL service
docker-entrypoint.sh postgres &

# Slave node setup
if [ "$POSTGRES_REPLICATION_ROLE" == "replica" ]; then
  echo "Configuring replica node..."
  until pg_isready -h master -p 5432 -U postgres; do
    echo "Waiting for master to be ready..."
    sleep 2
  done
  rm -rf $PGDATA/*
  pg_basebackup -h master -D $PGDATA -U replica -v -P -W
  echo "standby_mode = 'on'" >> "$PGDATA/recovery.conf"
  echo "primary_conninfo = 'host=master port=5432 user=replica password=password'" >> "$PGDATA/recovery.conf"
fi

exec "$@"