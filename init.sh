#!/bin/bash
set -e

# Start SQL Server in background
echo "Starting SQL Server..."
/opt/mssql/bin/sqlservr &

# Wait until SQL Server is ready
echo "Waiting for SQL Server to be available..."
until /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "$SA_PASSWORD" -Q "SELECT 1" >/dev/null 2>&1; do
  sleep 5
done

echo "Dropping existing database if exists..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "$SA_PASSWORD" -Q "IF DB_ID('techstoreDB') IS NOT NULL DROP DATABASE techstoreDB;"

echo "Running schema script..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "$SA_PASSWORD" -i /usr/src/app/schema.sql

echo "Schema initialization completed."

# Wait on SQL Server process
wait
