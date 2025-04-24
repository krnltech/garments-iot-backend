-- init.sql

-- Create the metrics database if it doesn't exist
CREATE DATABASE metrics;

-- Connect to the metrics database
\connect metrics;

-- Now create your tables inside metrics
CREATE TABLE IF NOT EXISTS employees (
    time TIMESTAMPTZ NOT NULL,
    id VARCHAR(36) NOT NULL,
    machine_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (machine_id, time)
);

-- Bundles Table
CREATE TABLE IF NOT EXISTS bundles (
    time TIMESTAMPTZ NOT NULL,
    id VARCHAR(36) NOT NULL,
    machine_id INTEGER NOT NULL,
    employee_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (machine_id, time)
);

-- Create hypertables
SELECT create_hypertable('employees', 'time', if_not_exists => TRUE);
SELECT create_hypertable('bundles', 'time', if_not_exists => TRUE);


