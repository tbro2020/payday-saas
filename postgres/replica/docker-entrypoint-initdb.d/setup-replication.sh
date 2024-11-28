#!/bin/bash
set -e

# Create a standby.signal file to indicate this is a replica
touch /var/lib/postgresql/data/standby.signal

# Create recovery configuration
cat > /var/lib/postgresql/data/postgresql.auto.conf << EOF
# Auto-generated replica configuration
primary_conninfo = 'host=primary port=5432 user=payday password=payday application_name=replica'
promote_trigger_file = '/tmp/postgresql.trigger'
recovery_target_timeline = 'latest'
EOF