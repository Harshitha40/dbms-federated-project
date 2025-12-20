-- ========================================
-- SAMPLE FEDERATED QUERIES
-- Federated Environmental Intelligence Platform
-- ========================================

-- These queries demonstrate Apache Drill's ability to query
-- across PostgreSQL, MongoDB, and CSV files

-- ========================================
-- BASIC QUERIES
-- ========================================

-- Query 1: List all regions from PostgreSQL
SELECT * FROM postgres.public.`Region_Info`;

-- Query 2: Get recent climate data
SELECT 
    climate_id,
    region_id,
    temperature,
    rainfall,
    humidity,
    timestamp
FROM postgres.public.`Climate_Data`
ORDER BY timestamp DESC
LIMIT 20;

-- Query 3: View biodiversity data from MongoDB
SELECT * FROM mongo.environmental_db.`Biodiversity_Data`;

-- Query 4: Query sensor readings from CSV
SELECT * FROM dfs.data.`sensor_readings.csv` LIMIT 10;

-- ========================================
-- JOIN QUERIES (PostgreSQL)
-- ========================================

-- Query 5: Climate data with region names
SELECT 
    r.region_name,
    r.latitude,
    r.longitude,
    c.temperature,
    c.rainfall,
    c.humidity,
    c.timestamp
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
ORDER BY c.timestamp DESC
LIMIT 20;

-- Query 6: Agriculture yields by region
SELECT 
    r.region_name,
    a.crop_type,
    a.yield,
    a.season,
    a.year
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Agriculture_Data` a ON r.region_id = a.region_id
ORDER BY a.yield DESC;

-- Query 7: Complete regional overview
SELECT 
    r.region_name,
    r.latitude,
    r.longitude,
    c.temperature,
    c.rainfall,
    c.humidity,
    a.crop_type,
    a.yield,
    a.season
FROM postgres.public.`Region_Info` r
LEFT JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
LEFT JOIN postgres.public.`Agriculture_Data` a ON r.region_id = a.region_id
WHERE c.temperature IS NOT NULL
LIMIT 50;

-- ========================================
-- AGGREGATION QUERIES
-- ========================================

-- Query 8: Average climate metrics by region
SELECT 
    r.region_name,
    AVG(c.temperature) as avg_temperature,
    AVG(c.rainfall) as avg_rainfall,
    AVG(c.humidity) as avg_humidity,
    COUNT(*) as measurement_count
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
GROUP BY r.region_name
ORDER BY avg_temperature DESC;

-- Query 9: Crop yields by season
SELECT 
    season,
    COUNT(*) as crop_count,
    SUM(yield) as total_yield,
    AVG(yield) as avg_yield,
    MAX(yield) as max_yield,
    MIN(yield) as min_yield
FROM postgres.public.`Agriculture_Data`
GROUP BY season
ORDER BY total_yield DESC;

-- Query 10: Top producing crops
SELECT 
    crop_type,
    COUNT(*) as regions_planted,
    AVG(yield) as avg_yield,
    SUM(yield) as total_yield
FROM postgres.public.`Agriculture_Data`
GROUP BY crop_type
ORDER BY total_yield DESC;

-- Query 11: Yearly agricultural trends
SELECT 
    year,
    season,
    COUNT(DISTINCT crop_type) as crop_variety,
    AVG(yield) as avg_yield
FROM postgres.public.`Agriculture_Data`
GROUP BY year, season
ORDER BY year DESC, season;

-- ========================================
-- FILTERING QUERIES
-- ========================================

-- Query 12: High temperature regions
SELECT 
    r.region_name,
    c.temperature,
    c.humidity,
    c.timestamp
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
WHERE c.temperature > 25
ORDER BY c.temperature DESC;

-- Query 13: Regions with high rainfall
SELECT 
    r.region_name,
    c.rainfall,
    c.temperature,
    c.timestamp
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
WHERE c.rainfall > 1000
ORDER BY c.rainfall DESC;

-- Query 14: Productive agriculture regions
SELECT 
    r.region_name,
    a.crop_type,
    a.yield,
    a.year
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Agriculture_Data` a ON r.region_id = a.region_id
WHERE a.yield > 20
ORDER BY a.yield DESC;

-- Query 15: Recent query logs by researchers
SELECT 
    u.name,
    u.email,
    q.query_text,
    q.executed_at
FROM postgres.public.`User_Info` u
JOIN postgres.public.`Query_Log` q ON u.user_id = q.user_id
WHERE u.role = 'Researcher'
ORDER BY q.executed_at DESC
LIMIT 10;

-- ========================================
-- MONGODB QUERIES
-- ========================================

-- Query 16: Biodiversity hotspots
SELECT 
    region_name,
    species_count,
    conservation_status,
    last_survey_date
FROM mongo.environmental_db.`Biodiversity_Data`
WHERE species_count > 5000
ORDER BY species_count DESC;

-- Query 17: Endangered species tracking
SELECT 
    region_name,
    endangered_species,
    conservation_status
FROM mongo.environmental_db.`Biodiversity_Data`
WHERE conservation_status = 'Critical';

-- Query 18: Sensor logs by severity
SELECT 
    sensor_id,
    region_id,
    event_type,
    severity,
    message,
    timestamp
FROM mongo.environmental_db.`Sensor_Logs`
WHERE severity = 'critical'
ORDER BY timestamp DESC;

-- Query 19: Air quality summary
SELECT 
    region_id,
    aqi,
    air_quality_level,
    recorded_at
FROM mongo.environmental_db.`Air_Quality_History`
ORDER BY aqi DESC;

-- Query 20: Active sensors metadata
SELECT 
    sensor_id,
    sensor_type,
    region_name,
    status,
    last_maintenance
FROM mongo.environmental_db.`Sensor_Metadata`
WHERE status = 'active'
ORDER BY last_maintenance DESC;

-- ========================================
-- CSV FILE QUERIES
-- ========================================

-- Query 21: Recent sensor readings
SELECT 
    timestamp,
    region_id,
    CAST(co2_level AS FLOAT) as co2_level,
    CAST(pm2_5 AS FLOAT) as pm2_5
FROM dfs.data.`sensor_readings.csv`
ORDER BY timestamp DESC
LIMIT 20;

-- Query 22: Average CO2 by region
SELECT 
    region_id,
    COUNT(*) as reading_count,
    AVG(CAST(co2_level AS FLOAT)) as avg_co2,
    MAX(CAST(co2_level AS FLOAT)) as max_co2,
    MIN(CAST(co2_level AS FLOAT)) as min_co2
FROM dfs.data.`sensor_readings.csv`
GROUP BY region_id
ORDER BY avg_co2 DESC;

-- Query 23: Air pollution levels (PM2.5)
SELECT 
    region_id,
    AVG(CAST(pm2_5 AS FLOAT)) as avg_pm25,
    MAX(CAST(pm2_5 AS FLOAT)) as max_pm25
FROM dfs.data.`sensor_readings.csv`
GROUP BY region_id
ORDER BY avg_pm25 DESC;

-- Query 24: High pollution alerts
SELECT 
    timestamp,
    region_id,
    CAST(co2_level AS FLOAT) as co2_level,
    CAST(pm2_5 AS FLOAT) as pm2_5
FROM dfs.data.`sensor_readings.csv`
WHERE CAST(pm2_5 AS FLOAT) > 50
ORDER BY CAST(pm2_5 AS FLOAT) DESC;

-- ========================================
-- ADVANCED FEDERATED QUERIES
-- ========================================

-- Query 25: Climate vs Agriculture correlation
-- Note: This query joins PostgreSQL tables
SELECT 
    r.region_name,
    AVG(c.temperature) as avg_temp,
    AVG(c.rainfall) as avg_rainfall,
    AVG(a.yield) as avg_yield,
    COUNT(DISTINCT a.crop_type) as crop_diversity
FROM postgres.public.`Region_Info` r
LEFT JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
LEFT JOIN postgres.public.`Agriculture_Data` a ON r.region_id = a.region_id
GROUP BY r.region_name
HAVING AVG(c.temperature) IS NOT NULL
ORDER BY avg_yield DESC;

-- Query 26: Comprehensive environmental summary
SELECT 
    r.region_name,
    r.latitude,
    r.longitude,
    COUNT(DISTINCT c.climate_id) as climate_records,
    AVG(c.temperature) as avg_temperature,
    COUNT(DISTINCT a.agri_id) as agriculture_records,
    AVG(a.yield) as avg_yield
FROM postgres.public.`Region_Info` r
LEFT JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
LEFT JOIN postgres.public.`Agriculture_Data` a ON r.region_id = a.region_id
GROUP BY r.region_name, r.latitude, r.longitude
ORDER BY r.region_name;

-- Query 27: Seasonal climate patterns
SELECT 
    CASE 
        WHEN EXTRACT(MONTH FROM c.timestamp) IN (12, 1, 2) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM c.timestamp) IN (3, 4, 5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM c.timestamp) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Fall'
    END as season,
    AVG(c.temperature) as avg_temperature,
    AVG(c.rainfall) as avg_rainfall,
    AVG(c.humidity) as avg_humidity
FROM postgres.public.`Climate_Data` c
GROUP BY season
ORDER BY avg_temperature DESC;

-- Query 28: Top regions by multiple criteria
SELECT 
    r.region_name,
    AVG(c.temperature) as avg_temp,
    AVG(c.rainfall) as avg_rainfall,
    AVG(a.yield) as avg_yield,
    COUNT(c.climate_id) as data_points
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
LEFT JOIN postgres.public.`Agriculture_Data` a ON r.region_id = a.region_id
GROUP BY r.region_name
HAVING COUNT(c.climate_id) > 0
ORDER BY avg_yield DESC, avg_temp DESC
LIMIT 10;

-- Query 29: User activity summary
SELECT 
    u.name,
    u.role,
    COUNT(q.query_id) as total_queries,
    MIN(q.executed_at) as first_query,
    MAX(q.executed_at) as last_query
FROM postgres.public.`User_Info` u
LEFT JOIN postgres.public.`Query_Log` q ON u.user_id = q.user_id
GROUP BY u.name, u.role
ORDER BY total_queries DESC;

-- Query 30: Data quality check
-- Count records in each data source
SELECT 'PostgreSQL - Region_Info' as source, COUNT(*) as record_count 
FROM postgres.public.`Region_Info`
UNION ALL
SELECT 'PostgreSQL - Climate_Data' as source, COUNT(*) as record_count 
FROM postgres.public.`Climate_Data`
UNION ALL
SELECT 'PostgreSQL - Agriculture_Data' as source, COUNT(*) as record_count 
FROM postgres.public.`Agriculture_Data`
UNION ALL
SELECT 'PostgreSQL - User_Info' as source, COUNT(*) as record_count 
FROM postgres.public.`User_Info`;

-- ========================================
-- NOTES ON FEDERATED QUERIES
-- ========================================

/*
1. Table names must be enclosed in backticks: `table_name`

2. Full path format:
   - PostgreSQL: postgres.public.`table_name`
   - MongoDB: mongo.database_name.`collection_name`
   - CSV: dfs.workspace_name.`file_name.csv`

3. Cross-database joins may have limitations:
   - Joins within same database work best
   - Cross-database joins may require subqueries
   - Consider performance for large datasets

4. Data type casting:
   - CSV columns are strings by default
   - Use CAST(column AS TYPE) for proper types
   - Example: CAST(co2_level AS FLOAT)

5. MongoDB queries:
   - Complex nested queries may not work
   - Stick to simple SELECT, WHERE, ORDER BY
   - Use MongoDB shell for complex queries

6. Performance tips:
   - Use LIMIT for testing queries
   - Add WHERE clauses to filter data
   - Index frequently queried columns
   - Use EXPLAIN PLAN to analyze queries
*/
