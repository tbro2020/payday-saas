#!/bin/bash

set -e

# Ensure the script is executable
chmod +x /docker-entrypoint-initdb.d/entrypoint.sh

# Master node setup
if [ "$POSTGRES_REPLICATION_ROLE" == "master" ]; then
  echo "Configuring master node..."
  echo "host replication all all md5" >> "$PGDATA/pg_hba.conf"
  echo "wal_level = replica" >> "$PGDATA/postgresql.conf"
  echo "max_wal_senders = 5" >> "$PGDATA/postgresql.conf"
  echo "wal_keep_size = 64" >> "$PGDATA/postgresql.conf"
  echo "archive_mode = on" >> "$PGDATA/postgresql.conf"
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
  pg_basebackup -h master -D $PGDATA -U postgres -v -P -W
  echo "standby_mode = 'on'" >> "$PGDATA/recovery.conf"
  echo "primary_conninfo = 'host=master port=5432 user=postgres password=password'" >> "$PGDATA/recovery.conf"
fi

exec "$@"
