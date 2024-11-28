#!/bin/bash
set -e

until pg_isready -h master -p 5432 -U replicator; do
  echo "Waiting for master to be ready..."
  sleep 2
done

PGDATA="/var/lib/postgresql/data"
rm -rf ${PGDATA}/*
pg_basebackup -h master -D ${PGDATA} -U replicator -Fp -Xs -R
exec postgres