-- Check if the 'payday' role exists. If it does, alter it; otherwise, create it.
DO $$ 
BEGIN
    -- Check if the role exists
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'payday') THEN
        -- If the role does not exist, create it with login and replication privileges
        CREATE ROLE payday WITH LOGIN PASSWORD 'payday' REPLICATION;
    ELSE
        -- If the role exists, grant it replication privileges and make it a superuser
        ALTER ROLE payday WITH REPLICATION SUPERUSER;
    END IF;
END $$;

-- Allow external connections
ALTER SYSTEM SET listen_addresses = '*';

-- Configure replication settings
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_replication_slots = 4;
ALTER SYSTEM SET max_wal_senders = 4;

-- Set the max_wal_size in bytes (2GB = 2147483648 bytes)
ALTER SYSTEM SET max_wal_size = 2147483648;

-- Reload PostgreSQL configuration to apply changes
SELECT pg_reload_conf();