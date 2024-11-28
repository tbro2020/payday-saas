-- Create the 'payday' role with replication privileges
CREATE ROLE payday WITH LOGIN PASSWORD 'payday' REPLICATION;

-- Grant the 'payday' role necessary permissions
GRANT ALL PRIVILEGES ON DATABASE payday TO payday;

-- Allow replication connections
ALTER SYSTEM SET listen_addresses = '*';  -- Allows external connections

-- Configure replication settings
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_replication_slots = 4;
ALTER SYSTEM SET max_wal_senders = 4;
ALTER SYSTEM SET max_wal_size = 2GB;

-- Reload PostgreSQL configuration
SELECT pg_reload_conf();