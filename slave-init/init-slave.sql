-- Configure the slave to connect to the master
ALTER SYSTEM SET primary_conninfo = 'host=master port=5432 user=payday password=payday sslmode=prefer';
ALTER SYSTEM SET primary_slot_name = 'replication_slot';

-- Place the standby.signal file
\! cp /tmp/standby.signal /var/lib/postgresql/data/standby.signal

-- Reload PostgreSQL configuration
SELECT pg_reload_conf();