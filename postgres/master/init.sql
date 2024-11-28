# postgres/master/init.sql
-- Create replication user
CREATE USER replicator WITH REPLICATION PASSWORD 'replicator_password';

-- Create application database
CREATE DATABASE payday;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE payday TO payday;