-- Configure slave to replicate from master
ALTER SYSTEM SET primary_conninfo = 'host=master port=5432 user=payday password=payday sslmode=prefer';
ALTER SYSTEM SET primary_slot_name = 'replication_slot';

-- Reload PostgreSQL configuration
SELECT pg_reload_conf();