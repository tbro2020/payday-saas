# postgres/slave/Dockerfile
FROM postgres:15

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/
COPY pg_hba.conf /etc/postgresql/pg_hba.conf
COPY postgresql.conf /etc/postgresql/postgresql.conf

# Expose PostgreSQL default port
EXPOSE 5432