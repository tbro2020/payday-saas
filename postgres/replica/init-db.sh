#!/bin/bash
set -e

# Check if POSTGRES_MULTIPLE_DATABASES is set
if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
    echo "Creating multiple databases: $POSTGRES_MULTIPLE_DATABASES"
    
    # Convert comma-separated list to array
    IFS=',' read -r -a databases <<< "$POSTGRES_MULTIPLE_DATABASES"
    
    # Create each database
    for db in "${databases[@]}"; do
        echo "Creating database: $db"
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
            CREATE DATABASE "$db" WITH OWNER = "$POSTGRES_USER";
            GRANT ALL PRIVILEGES ON DATABASE "$db" TO "$POSTGRES_USER";
EOSQL
    done
fi