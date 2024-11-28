#!/bin/bash
set -e

# Add pg_hba.conf entries
echo "local   all             all                                     trust" >> /var/lib/postgresql/data/pg_hba.conf
echo "host    all             all             0.0.0.0/0               md5" >> /var/lib/postgresql/data/pg_hba.conf
echo "host    replication     payday          0.0.0.0/0               md5" >> /var/lib/postgresql/data/pg_hba.conf

# Start PostgreSQL
exec docker-entrypoint.sh postgres