-- init.sql

-- Create the metrics database if it doesn't exist
CREATE DATABASE metrics;

-- Connect to the metrics database
\connect metrics;

-- Users Table (for authentication)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Now create your tables inside metrics
CREATE TABLE IF NOT EXISTS worker_scan (  -- instead of workerScan
    time TIMESTAMPTZ NOT NULL,
    id VARCHAR(36) NOT NULL,
    machine_id VARCHAR(36) NOT NULL,
    name TEXT NOT NULL
);

-- Bundles Table
CREATE TABLE IF NOT EXISTS bundle(
    time TIMESTAMPTZ NOT NULL,
    id VARCHAR(36) NOT NULL,
    machine_id VARCHAR(36) NOT NULL,
    employee_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (machine_id, time)
);

-- Machine Table
CREATE TABLE IF NOT EXISTS machine (
    id SERIAL PRIMARY KEY,
    label VARCHAR(36) NOT NULL,
    location VARCHAR(36) NOT NULL
);

-- Machine Target Table
CREATE TABLE IF NOT EXISTS machine_target (
    id_machine INTEGER NOT NULL,
    target INTEGER NOT NULL,
    PRIMARY KEY (id_machine),
    FOREIGN KEY (id_machine) REFERENCES machine(id) ON DELETE CASCADE
);

-- Worker Table
CREATE TABLE IF NOT EXISTS worker (
    id SERIAL PRIMARY KEY,
    name VARCHAR(36) NOT NULL,
    designation VARCHAR(36) NOT NULL
);

-- Worker Target Table
CREATE TABLE IF NOT EXISTS worker_target (
    id_worker INTEGER NOT NULL,
    target INTEGER NOT NULL,
    PRIMARY KEY (id_worker),
    FOREIGN KEY (id_worker) REFERENCES worker(id) ON DELETE CASCADE
);

-- Create hypertables
SELECT create_hypertable('worker_scan', 'time', if_not_exists => TRUE);
SELECT create_hypertable('bundle', 'time', if_not_exists => TRUE);


