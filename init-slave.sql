-- Set the slave to start replication using the 'payday' role
-- The slave will connect to the master and begin replication
SELECT pg_create_physical_replication_slot('replication_slot');