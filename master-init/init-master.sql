-- Create role 'payday' for replication with superuser rights
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'payday') THEN
        CREATE ROLE payday WITH LOGIN PASSWORD 'payday' REPLICATION SUPERUSER;
    ELSE
        ALTER ROLE payday WITH REPLICATION SUPERUSER;
    END IF;
END $$;

-- PostgreSQL settings for replication
ALTER SYSTEM SET listen_addresses = '*';
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET max_wal_size = '2GB';

-- Create replication slot
SELECT pg_create_physical_replication_slot('replication_slot');

-- Reload PostgreSQL configuration
SELECT pg_reload_conf();