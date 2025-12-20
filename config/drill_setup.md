# ========================================
# APACHE DRILL SETUP AND CONFIGURATION
# Federated Query Engine Setup Guide
# ========================================

## STEP 1: Verify Apache Drill Installation
# Open PowerShell and navigate to your Drill installation directory
# Example: cd C:\drill\apache-drill-x.xx.x

## STEP 2: Start Apache Drill
# Run in embedded mode (for development):
bin\drill-embedded.bat

# OR run in distributed mode:
# bin\drillbit.bat start

## STEP 3: Access Drill Web UI
# Open browser and go to: http://localhost:8047
# This is the Drill Web Console

## STEP 4: Configure Storage Plugins

### PostgreSQL Storage Plugin Configuration
# 1. Go to http://localhost:8047/storage
# 2. Click "Update" next to "postgres" or create new plugin named "postgres"
# 3. Use this configuration:

{
  "type": "jdbc",
  "driver": "org.postgresql.Driver",
  "url": "jdbc:postgresql://localhost:5432/environmental_db",
  "username": "postgres",
  "password": "postgres",
  "enabled": true
}

# NOTE: You need to download PostgreSQL JDBC driver
# Download from: https://jdbc.postgresql.org/download/
# Place the JAR file in: apache-drill/jars/3rdparty/

### MongoDB Storage Plugin Configuration
# 1. Click "Update" next to "mongo" or create new plugin named "mongo"
# 2. Use this configuration:

{
  "type": "mongo",
  "connection": "mongodb://localhost:27017/",
  "enabled": true
}

### CSV File Storage Plugin (DFS - Distributed File System)
# The default "dfs" plugin should work for CSV files
# Update the "dfs" plugin configuration:
# 1. Click "Update" next to "dfs"
# 2. Add your CSV file location in the "workspaces" section

{
  "type": "file",
  "connection": "file:///",
  "workspaces": {
    "root": {
      "location": "/",
      "writable": false,
      "defaultInputFormat": null
    },
    "tmp": {
      "location": "/tmp",
      "writable": true,
      "defaultInputFormat": null
    },
    "data": {
      "location": "C:/Users/Lenovo/dbmsel/proj/data",
      "writable": false,
      "defaultInputFormat": "csv"
    }
  },
  "formats": {
    "csv": {
      "type": "text",
      "extensions": ["csv"],
      "delimiter": ",",
      "extractHeader": true
    }
  },
  "enabled": true
}

## STEP 5: Test Connections

# Test PostgreSQL connection:
SELECT * FROM postgres.public.`Region_Info` LIMIT 5;

# Test MongoDB connection:
SELECT * FROM mongo.environmental_db.`Biodiversity_Data` LIMIT 5;

# Test CSV file:
SELECT * FROM dfs.data.`sensor_readings.csv` LIMIT 5;

## STEP 6: Sample Federated Queries

# Query 1: Join PostgreSQL tables
SELECT 
    r.region_name,
    c.temperature,
    c.rainfall,
    c.humidity
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
LIMIT 10;

# Query 2: Join PostgreSQL with MongoDB
# Note: Cross-database joins may have limitations
SELECT 
    r.region_name,
    r.latitude,
    r.longitude
FROM postgres.public.`Region_Info` r
LIMIT 10;

# Query 3: Query CSV data
SELECT 
    region_id,
    AVG(CAST(co2_level AS FLOAT)) as avg_co2,
    AVG(CAST(pm2_5 AS FLOAT)) as avg_pm25
FROM dfs.data.`sensor_readings.csv`
GROUP BY region_id;

## TROUBLESHOOTING

# Issue: PostgreSQL JDBC Driver Not Found
# Solution: Download postgresql-42.x.x.jar from https://jdbc.postgresql.org/download/
# Place in: apache-drill/jars/3rdparty/

# Issue: MongoDB Plugin Not Working
# Solution: Ensure MongoDB is running (net start MongoDB)
# Check connection string: mongodb://localhost:27017/

# Issue: CSV File Not Found
# Solution: Use absolute path in DFS workspace configuration
# Ensure forward slashes: C:/Users/Lenovo/dbmsel/proj/data

# Issue: Drill Not Starting
# Solution: Check if port 8047 is already in use
# Check Java installation: java -version

## IMPORTANT NOTES

1. Apache Drill requires Java 8 or later
2. For Windows, use forward slashes (/) in file paths, not backslashes (\)
3. CSV files must have headers for extractHeader: true
4. Large result sets may be slow in federated queries
5. Some cross-database joins may not be supported (use subqueries instead)

## DRILL REST API

# Execute query via REST API (used by Flask backend):
POST http://localhost:8047/query.json
Content-Type: application/json

{
  "queryType": "SQL",
  "query": "SELECT * FROM postgres.public.`Region_Info` LIMIT 5"
}

# Check Drill status:
GET http://localhost:8047/status

## USEFUL DRILL COMMANDS

# Show all storage plugins:
SHOW DATABASES;

# Show tables in a plugin:
SHOW TABLES IN postgres.public;
SHOW TABLES IN mongo.environmental_db;

# Describe table structure:
DESCRIBE postgres.public.`Region_Info`;
