#!/bin/bash
set -e

# Allow replication connections from the slave container using the service name "master"
echo "host replication replicator master trust" >> /var/lib/postgresql/data/pg_hba.conf

# Optionally: Create the replicator role (if not already done in init.sql)
psql -U postgres -c "CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator_password';"

# Reload PostgreSQL to apply changes
pg_ctl reload -D /var/lib/postgresql/data

# Continue with the default entrypoint
exec "$@"