-- Wait for the master to be available
DO $$ 
BEGIN
    PERFORM pg_sleep(10);  -- Wait for some time before proceeding
END $$;

-- Place the standby.signal file after database initialization
-- This step will ensure that the slave enters standby mode
\! cp /tmp/standby.signal /var/lib/postgresql/data/standby.signal

-- Configure the slave to connect to the master
ALTER SYSTEM SET primary_conninfo = 'host=master port=5432 user=payday password=payday sslmode=prefer';
ALTER SYSTEM SET primary_slot_name = 'replication_slot';

-- Reload PostgreSQL configuration
SELECT pg_reload_conf();