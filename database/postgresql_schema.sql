-- ========================================
-- FEDERATED ENVIRONMENTAL INTELLIGENCE PLATFORM
-- PostgreSQL Schema Setup
-- ========================================

-- Drop existing tables (for clean setup)
DROP TABLE IF EXISTS Query_Log CASCADE;
DROP TABLE IF EXISTS Agriculture_Data CASCADE;
DROP TABLE IF EXISTS Climate_Data CASCADE;
DROP TABLE IF EXISTS Region_Info CASCADE;
DROP TABLE IF EXISTS User_Info CASCADE;

-- ========================================
-- TABLE 1: User_Info
-- Purpose: Store user credentials and roles for authentication
-- ========================================
CREATE TABLE User_Info (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('Researcher', 'Data Provider', 'Administrator')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- TABLE 2: Region_Info
-- Purpose: Store geographical regions for environmental data
-- ========================================
CREATE TABLE Region_Info (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL
);

-- ========================================
-- TABLE 3: Climate_Data
-- Purpose: Store climate measurements per region
-- Related to: Region_Info (region_id FK)
-- ========================================
CREATE TABLE Climate_Data (
    climate_id SERIAL PRIMARY KEY,
    region_id INTEGER NOT NULL,
    temperature DECIMAL(5, 2) NOT NULL,  -- in Celsius
    rainfall DECIMAL(6, 2) NOT NULL,     -- in mm
    humidity DECIMAL(5, 2) NOT NULL,     -- percentage
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region_id) REFERENCES Region_Info(region_id) ON DELETE CASCADE
);

-- ========================================
-- TABLE 4: Agriculture_Data
-- Purpose: Store agricultural yield data per region
-- Related to: Region_Info (region_id FK)
-- ========================================
CREATE TABLE Agriculture_Data (
    agri_id SERIAL PRIMARY KEY,
    region_id INTEGER NOT NULL,
    crop_type VARCHAR(50) NOT NULL,
    yield DECIMAL(10, 2) NOT NULL,       -- in tons
    season VARCHAR(20) CHECK (season IN ('Spring', 'Summer', 'Fall', 'Winter')) NOT NULL,
    year INTEGER NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Region_Info(region_id) ON DELETE CASCADE
);

-- ========================================
-- TABLE 5: Query_Log
-- Purpose: Log all federated queries executed by users
-- Related to: User_Info (user_id FK)
-- Used for: Audit trail and analytics
-- ========================================
CREATE TABLE Query_Log (
    query_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    query_text TEXT NOT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User_Info(user_id) ON DELETE CASCADE
);

-- ========================================
-- INSERT SAMPLE DATA
-- ========================================

-- Sample Users (password: 'password123' for all)
-- Password hash generated using bcrypt with salt rounds=12
INSERT INTO User_Info (name, email, password_hash, role) VALUES
('Dr. Sarah Johnson', 'sarah.researcher@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5OMKVVEqZE.Yi', 'Researcher'),
('Mike Data Provider', 'mike.provider@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5OMKVVEqZE.Yi', 'Data Provider'),
('Admin User', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5OMKVVEqZE.Yi', 'Administrator');

-- Sample Regions
INSERT INTO Region_Info (region_name, latitude, longitude) VALUES
('Amazon Basin', -3.4653, -62.2159),
('Great Barrier Reef', -18.2871, 147.6992),
('Sahara Desert', 23.8859, 8.0817),
('Arctic Tundra', 71.5388, -156.7889),
('Congo Rainforest', -0.2280, 15.8277),
('Himalayas', 28.5983, 83.9956),
('Great Plains', 41.4925, -99.9018),
('Madagascar', -18.7669, 46.8691);
('Patagonia', -49.3315, -72.8860),
('Andes Mountains', -13.1631, -72.5450),
('Gobi Desert', 42.5903, 103.4319),
('Yellowstone National Park', 44.4280, -110.5885),
('Sundarbans Mangrove Forest', 21.9497, 89.1833),
('Borneo Rainforest', 0.7893, 113.9213),
('Taiga Forest (Siberia)', 61.5240, 105.3188),
('Atacama Desert', -23.8634, -69.1328),
('Galápagos Islands', -0.9538, -90.9656),
('Scottish Highlands', 57.1200, -4.7100),
('Alps', 46.8182, 8.2275),
('Okavango Delta', -19.2870, 22.4430);


-- Sample Climate Data
INSERT INTO Climate_Data (region_id, temperature, rainfall, humidity, timestamp) VALUES
(1, 26.5, 2300.50, 85.3, '2024-01-15 08:00:00'),
(1, 27.2, 2450.75, 87.1, '2024-02-15 08:00:00'),
(2, 24.8, 1800.20, 78.5, '2024-01-15 08:00:00'),
(2, 25.1, 1920.40, 79.2, '2024-02-15 08:00:00'),
(3, 38.4, 50.10, 15.2, '2024-01-15 08:00:00'),
(3, 40.2, 45.30, 12.8, '2024-02-15 08:00:00'),
(4, -25.3, 150.80, 65.4, '2024-01-15 08:00:00'),
(4, -22.1, 180.20, 68.1, '2024-02-15 08:00:00'),
(5, 24.9, 1500.60, 82.7, '2024-01-15 08:00:00'),
(6, 15.2, 1200.40, 70.5, '2024-01-15 08:00:00'),
(7, 18.5, 600.25, 55.3, '2024-01-15 08:00:00'),
(8, 22.1, 1400.90, 75.8, '2024-01-15 08:00:00');
(9, 6.4, 520.30, 68.2, '2024-01-15 08:00:00'),     -- Patagonia
(10, 12.8, 980.75, 72.5, '2024-01-15 08:00:00'),  -- Andes Mountains
(11, -4.6, 180.40, 41.3, '2024-01-15 08:00:00'),  -- Gobi Desert
(12, 2.1, 760.90, 65.7, '2024-01-15 08:00:00'),   -- Yellowstone
(13, 26.9, 2100.60, 88.9, '2024-01-15 08:00:00'), -- Sundarbans
(14, 27.3, 2450.20, 90.4, '2024-01-15 08:00:00'), -- Borneo Rainforest
(15, -8.2, 430.10, 55.6, '2024-01-15 08:00:00'),  -- Siberian Taiga
(16, 18.7, 22.40, 19.8, '2024-01-15 08:00:00'),   -- Atacama Desert
(17, 24.5, 610.85, 77.2, '2024-01-15 08:00:00'),  -- Galápagos
(18, 5.9, 1350.40, 81.6, '2024-01-15 08:00:00'),  -- Scottish Highlands
(19, -1.8, 1180.30, 69.1, '2024-01-15 08:00:00'), -- Alps
(20, 29.4, 690.75, 64.8, '2024-01-15 08:00:00');  -- Okavango Delta


-- Sample Agriculture Data
INSERT INTO Agriculture_Data (region_id, crop_type, yield, season, year) VALUES
(1, 'Cassava', 15.8, 'Summer', 2023),
(1, 'Cocoa', 8.5, 'Fall', 2023),
(5, 'Cassava', 12.3, 'Summer', 2023),
(5, 'Plantain', 10.7, 'Spring', 2023),
(7, 'Wheat', 45.2, 'Summer', 2023),
(7, 'Corn', 52.8, 'Fall', 2023),
(7, 'Soybean', 38.6, 'Summer', 2023),
(8, 'Rice', 30.4, 'Spring', 2023),
(8, 'Vanilla', 2.1, 'Fall', 2023),
(6, 'Barley', 15.3, 'Summer', 2023);
(9,  'Sheep Grazing',  1.85, 'Summer', 2023),   -- Patagonia
(10, 'Potatoes',      3.20, 'Autumn', 2023),   -- Andes Mountains
(11, 'Barley',        1.10, 'Spring', 2023),   -- Gobi (irrigated pockets)
(12, 'Wheat',         4.75, 'Summer', 2023),   -- Yellowstone region
(8, 'Rice',          6.90, 'Monsoon', 2023),  -- Sundarbans
(14, 'Oil Palm',      4.60, 'Annual',  2023),  -- Borneo Rainforest
(15, 'Rye',           2.30, 'Summer', 2023),   -- Siberian Taiga
(15, 'Quinoa',        0.95, 'Winter',  2023),  -- Atacama (oasis farming)
(7, 'Banana',        7.80, 'Annual',  2023),  -- Galápagos (limited zones)
(18, 'Barley',        3.60, 'Spring',  2023),  -- Scottish Highlands
(19, 'Grapes',        5.40, 'Autumn',  2023),  -- Alps
(20, 'Maize',         4.20, 'Summer',  2023);  -- Okavango Delta


-- Sample Query Logs (for demonstration)
INSERT INTO Query_Log (user_id, query_text) VALUES
(1, 'SELECT * FROM postgres.public.Region_Info'),
(1, 'SELECT region_name, temperature FROM postgres.public.Climate_Data JOIN postgres.public.Region_Info ON Climate_Data.region_id = Region_Info.region_id'),
(3, 'SELECT * FROM postgres.public.User_Info');

-- ========================================
-- VERIFICATION QUERIES
-- ========================================
-- Run these to verify the setup:
-- SELECT * FROM User_Info;
-- SELECT * FROM Region_Info;
-- SELECT * FROM Climate_Data;
-- SELECT * FROM Agriculture_Data;
-- SELECT * FROM Query_Log;

COMMIT;
