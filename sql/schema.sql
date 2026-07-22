-- UrbanFlow: Pune Traffic & Congestion Analysis Schema Definition
-- Target DBMS: MySQL 8.0+

CREATE DATABASE IF NOT EXISTS urbanflow_pune;
USE urbanflow_pune;

-- Drop existing tables to support clean schema re-initialization
DROP TABLE IF EXISTS traffic_data;
DROP TABLE IF EXISTS vehicle_registrations;

-- Table 1: GTFS Traffic & Congestion Metrics
CREATE TABLE traffic_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    route_id VARCHAR(50) NOT NULL,
    stop_name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    time_slot VARCHAR(50) NOT NULL,
    speed_congested DECIMAL(6, 2) NOT NULL,
    speed_freeflow DECIMAL(6, 2) NOT NULL,
    sri DECIMAL(6, 2) NOT NULL COMMENT 'Speed Reduction Index (%)',
    congestion_level VARCHAR(50) NOT NULL,
    is_peak_hour TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_route (route_id),
    INDEX idx_stop (stop_name),
    INDEX idx_congestion (congestion_level),
    INDEX idx_peak (is_peak_hour)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 2: Pune Annual Vehicle Registrations (OpenCity Data)
CREATE TABLE vehicle_registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    vehicle_type VARCHAR(100) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    count INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year (year),
    INDEX idx_vehicle_type (vehicle_type),
    INDEX idx_fuel (fuel_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
