#!/bin/bash

set -e

# Master node setup
if [ "$POSTGRES_REPLICATION_ROLE" == "master" ]; then
  echo "Configuring master node..."
  echo "host replication all all md5" >> "$PGDATA/pg_hba.conf"
  echo "wal_level = replica" >> "$PGDATA/postgresql.conf"
  echo "max_wal_senders = 5" >> "$PGDATA/postgresql.conf"
  echo "wal_keep_size = 64" >> "$PGDATA/postgresql.conf"
  echo "archive_mode = on" >> "$PGDATA/postgresql.conf"
fi

# Slave node setup
if [ "$POSTGRES_REPLICATION_ROLE" == "replica" ]; then
  echo "Configuring replica node..."
  rm -rf $PGDATA/*
  pg_basebackup -h master -D $PGDATA -U postgres -v -P -W
  echo "standby_mode = 'on'" >> "$PGDATA/recovery.conf"
  echo "primary_conninfo = 'host=master port=5432 user=postgres password=password'" >> "$PGDATA/recovery.conf"
fi

exec "$@"