# Federated Environmental Intelligence Platform

A complete full-stack federated DBMS application that integrates heterogeneous data sources (PostgreSQL, MongoDB, and CSV) using Apache Drill as the federated query engine.

## 🌟 Features

- **Federated Query Engine**: Query across SQL, NoSQL, and CSV files seamlessly
- **Role-Based Access Control**: Three user roles with different permissions
- **Authentication & Authorization**: Secure session-based authentication with bcrypt
- **Modern Web UI**: Clean HTML/CSS/JavaScript frontend (no frameworks)
- **RESTful API**: Flask backend with comprehensive endpoints
- **Real-Time Data Management**: Insert and update environmental data
- **Admin Dashboard**: User management and query logging

## 📋 Table of Contents

- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Database Setup](#database-setup)
- [Apache Drill Configuration](#apache-drill-configuration)
- [Running the Application](#running-the-application)
- [User Roles](#user-roles)
- [Sample Queries](#sample-queries)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser (Frontend)                │
│              HTML + CSS + Vanilla JavaScript            │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────┐
│                  Flask Backend Server                    │
│        Authentication │ Authorization │ Routing         │
└─────────┬──────────────────────────────────┬────────────┘
          │                                  │
          │ Federated Queries               │ Direct Queries
          │                                  │
┌─────────▼──────────────┐       ┌──────────▼─────────────┐
│   Apache Drill         │       │   Database Manager     │
│ (Federated Layer)      │       │  (Direct Connections)  │
└─────────┬──────────────┘       └──────────┬─────────────┘
          │                                  │
    ┌─────┴─────┬──────────────┬────────────┴──────┐
    │           │              │                   │
┌───▼────┐ ┌───▼────┐  ┌──────▼─────┐   ┌────────▼──────┐
│PostgreSQL MongoDB │  │  CSV Files │   │ Session Store │
│(Relational)NoSQL │  │ (Sensors)  │   └───────────────┘
└─────────┘ └────────┘  └────────────┘
```

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8+**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

2. **PostgreSQL 12+**
   - Download: https://www.postgresql.org/download/
   - Default port: 5432

3. **MongoDB 4.4+**
   - Download: https://www.mongodb.com/try/download/community
   - Default port: 27017

4. **Apache Drill 1.20+**
   - Download: https://drill.apache.org/download/
   - Requires Java 8 or later
   - Default port: 8047

5. **Java 8 or later** (for Apache Drill)
   - Download: https://adoptium.net/
   - Verify: `java -version`

## 📦 Installation Guide

### Step 1: Clone/Navigate to Project Directory

```powershell
cd C:\Users\Lenovo\dbmsel\proj
```

### Step 2: Install Python Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

Required packages:
- Flask 3.0.0
- Flask-CORS 4.0.0
- psycopg2-binary 2.9.9
- pymongo 4.6.1
- bcrypt 4.1.2
- requests 2.31.0

## 🗄️ Database Setup

### PostgreSQL Setup

1. **Start PostgreSQL service:**
```powershell
# Start service (as Administrator)
net start postgresql-x64-14
```

2. **Create database and tables:**
```powershell
# Connect to PostgreSQL
psql -U postgres

# In psql prompt:
CREATE DATABASE environmental_db;
\c environmental_db

# Run schema file
\i C:/Users/Lenovo/dbmsel/proj/database/postgresql_schema.sql

# Verify
\dt
SELECT * FROM User_Info;
\q
```

3. **Update backend configuration:**
Edit `backend/config.py` and set your PostgreSQL password:
```python
POSTGRES_CONFIG = {
    'password': 'your_actual_postgres_password'
}
```

### MongoDB Setup

1. **Start MongoDB service:**
```powershell
# Start service (as Administrator)
net start MongoDB
```

2. **Load sample data:**
```powershell
# Connect to MongoDB shell
mongosh

# Load the setup script
load("C:/Users/Lenovo/dbmsel/proj/database/mongodb_setup.js")

# Verify
use environmental_db
show collections
db.Biodiversity_Data.find().pretty()
exit
```

## 🔗 Apache Drill Configuration

### Step 1: Start Apache Drill

```powershell
# Navigate to Drill installation directory
cd C:\drill\apache-drill-x.xx.x

# Start in embedded mode
bin\drill-embedded.bat
```

### Step 2: Configure Storage Plugins

1. **Open Drill Web UI:**
   - Browser: http://localhost:8047
   - Go to: Storage tab

2. **Configure PostgreSQL Plugin:**
   - Click "Create" or "Update" for plugin named `postgres`
   - Paste this configuration:

```json
{
  "type": "jdbc",
  "driver": "org.postgresql.Driver",
  "url": "jdbc:postgresql://localhost:5432/environmental_db",
  "username": "postgres",
  "password": "your_postgres_password",
  "enabled": true
}
```

**Important:** Download PostgreSQL JDBC driver:
- URL: https://jdbc.postgresql.org/download/
- File: postgresql-42.x.x.jar
- Place in: `apache-drill/jars/3rdparty/`

3. **Configure MongoDB Plugin:**
   - Update plugin named `mongo`:

```json
{
  "type": "mongo",
  "connection": "mongodb://localhost:27017/",
  "enabled": true
}
```

4. **Configure CSV File Plugin (DFS):**
   - Update `dfs` plugin, add this workspace:

```json
{
  "type": "file",
  "connection": "file:///",
  "workspaces": {
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
```

### Step 3: Test Drill Connections

In Drill Web UI, go to Query tab and test:

```sql
-- Test PostgreSQL
SELECT * FROM postgres.public.`Region_Info` LIMIT 5;

-- Test MongoDB
SELECT * FROM mongo.environmental_db.`Biodiversity_Data` LIMIT 5;

-- Test CSV
SELECT * FROM dfs.data.`sensor_readings.csv` LIMIT 5;
```

## 🚀 Running the Application

### Start All Services

1. **PostgreSQL**: Already running (Step 1 of Database Setup)
2. **MongoDB**: Already running (Step 1 of MongoDB Setup)
3. **Apache Drill**: Already running (Step 1 of Drill Configuration)

### Start Flask Backend

```powershell
cd C:\Users\Lenovo\dbmsel\proj\backend
python app.py
```

You should see:
```
==================================================
FEDERATED ENVIRONMENTAL INTELLIGENCE PLATFORM
==================================================

Initializing database connections...
PostgreSQL: ✓ Connected
MongoDB: ✓ Connected
Apache Drill: ✓ Connected

==================================================
Starting Flask server...
Access the application at: http://localhost:5000
==================================================
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 👥 User Roles

### 1. Researcher
**Email:** sarah.researcher@example.com  
**Password:** password123

**Permissions:**
- Execute federated queries
- View analytics dashboard
- Access query interface
- Cannot insert/update data
- Cannot access admin panel

### 2. Data Provider
**Email:** mike.provider@example.com  
**Password:** password123

**Permissions:**
- Insert climate data (PostgreSQL)
- Insert agriculture data (PostgreSQL)
- Insert sensor logs (MongoDB)
- Cannot execute federated queries
- Cannot access admin panel

### 3. Administrator
**Email:** admin@example.com  
**Password:** password123

**Permissions:**
- Full access to all features
- User management (create/delete users)
- View query logs
- Execute federated queries
- Insert/update data
- Access all dashboards

## 📊 Sample Queries

### Query 1: Basic PostgreSQL Query
```sql
SELECT * FROM postgres.public.`Region_Info` LIMIT 10;
```

### Query 2: Join PostgreSQL Tables
```sql
SELECT 
    r.region_name,
    c.temperature,
    c.rainfall,
    c.humidity
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
LIMIT 10;
```

### Query 3: MongoDB Query
```sql
SELECT 
    region_name,
    species_count,
    conservation_status
FROM mongo.environmental_db.`Biodiversity_Data`
WHERE species_count > 5000;
```

### Query 4: CSV File Query
```sql
SELECT 
    region_id,
    AVG(CAST(co2_level AS FLOAT)) as avg_co2,
    AVG(CAST(pm2_5 AS FLOAT)) as avg_pm25
FROM dfs.data.`sensor_readings.csv`
GROUP BY region_id;
```

### Query 5: Complex Federated Join
```sql
SELECT 
    r.region_name,
    r.latitude,
    r.longitude,
    c.temperature,
    a.crop_type,
    a.yield
FROM postgres.public.`Region_Info` r
LEFT JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
LEFT JOIN postgres.public.`Agriculture_Data` a ON r.region_id = a.region_id
WHERE c.temperature > 20
LIMIT 20;
```

### Query 6: Aggregation Query
```sql
SELECT 
    season,
    COUNT(*) as crop_count,
    AVG(yield) as avg_yield
FROM postgres.public.`Agriculture_Data`
GROUP BY season
ORDER BY avg_yield DESC;
```

## 📁 Project Structure

```
proj/
│
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── auth.py                # Authentication & authorization
│   ├── database.py            # Database connection modules
│   ├── config.py              # Configuration settings
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── login.html             # Login page
│   ├── login.js               # Login logic
│   ├── dashboard.html         # Main dashboard
│   ├── dashboard.js           # Dashboard logic
│   ├── query.html             # Federated query interface
│   ├── query.js               # Query execution logic
│   ├── data-provider.html     # Data management page
│   ├── data-provider.js       # Data insertion logic
│   ├── admin.html             # Admin panel
│   ├── admin.js               # Admin functions
│   └── style.css              # Main stylesheet
│
├── database/
│   ├── postgresql_schema.sql  # PostgreSQL schema & data
│   ├── postgresql_setup.md    # PostgreSQL setup guide
│   ├── mongodb_setup.js       # MongoDB collections & data
│   └── mongodb_setup.md       # MongoDB setup guide
│
├── data/
│   └── sensor_readings.csv    # CSV sensor data
│
├── config/
│   └── drill_setup.md         # Apache Drill configuration
│
└── README.md                  # This file
```

## 📡 API Documentation

### Authentication Endpoints

#### POST /api/login
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "name": "User Name",
    "email": "user@example.com",
    "role": "Researcher"
  }
}
```

#### POST /api/logout
Logout current user.

#### GET /api/current-user
Get current logged-in user information.

### Query Endpoints

#### POST /api/federated-query
Execute a federated SQL query (Researcher & Admin only).

**Request:**
```json
{
  "query": "SELECT * FROM postgres.public.`Region_Info` LIMIT 10"
}
```

**Response:**
```json
{
  "success": true,
  "data": [...],
  "columns": [...]
}
```

#### GET /api/sample-queries
Get sample federated queries.

### Data Provider Endpoints

#### POST /api/insert-climate
Insert climate data (Data Provider & Admin only).

**Request:**
```json
{
  "region_id": 1,
  "temperature": 25.5,
  "rainfall": 1500.0,
  "humidity": 80.5
}
```

#### POST /api/insert-agriculture
Insert agriculture data.

#### POST /api/insert-sensor-log
Insert sensor log into MongoDB.

### Admin Endpoints

#### GET /api/users
Get all users (Admin only).

#### POST /api/users
Create new user (Admin only).

#### DELETE /api/users/:id
Delete user (Admin only).

#### GET /api/query-logs
Get query execution logs (Admin only).

### Utility Endpoints

#### GET /api/database-status
Check connection status of all databases.

#### GET /api/regions
Get list of all regions.

## 🔍 Troubleshooting

### Issue: PostgreSQL Connection Failed

**Solution:**
1. Check if PostgreSQL is running: `net start postgresql-x64-14`
2. Verify password in `backend/config.py`
3. Test connection: `psql -U postgres -d environmental_db`

### Issue: MongoDB Connection Failed

**Solution:**
1. Check if MongoDB is running: `net start MongoDB`
2. Verify connection: `mongosh`
3. Check port 27017 is not blocked

### Issue: Apache Drill Not Responding

**Solution:**
1. Check if Drill is running: http://localhost:8047
2. Verify Java is installed: `java -version`
3. Check Drill logs in `apache-drill/log/`
4. Restart Drill: Close terminal and run `bin\drill-embedded.bat` again

### Issue: PostgreSQL JDBC Driver Not Found

**Solution:**
1. Download: https://jdbc.postgresql.org/download/postgresql-42.x.x.jar
2. Copy to: `apache-drill/jars/3rdparty/`
3. Restart Apache Drill

### Issue: Frontend Can't Connect to Backend

**Solution:**
1. Check Flask is running on port 5000
2. Check for CORS errors in browser console
3. Verify `API_BASE_URL` in JavaScript files is correct
4. Disable browser extensions that might block requests

### Issue: "Authentication Required" Error

**Solution:**
1. Clear browser cookies
2. Re-login with correct credentials
3. Check Flask session configuration in `config.py`

### Issue: Federated Query Fails

**Solution:**
1. Test query in Drill Web UI first (http://localhost:8047)
2. Verify all storage plugins are enabled
3. Check table names use backticks: \`table_name\`
4. Verify database/collection exists

## 🎓 Educational Concepts Demonstrated

This project demonstrates key DBMS concepts:

1. **Federated Database Systems**: Integration of heterogeneous data sources
2. **Query Optimization**: Apache Drill's distributed query execution
3. **Data Virtualization**: Querying without data centralization
4. **Authentication & Authorization**: Session-based security with bcrypt
5. **RESTful API Design**: Clean separation of concerns
6. **Database Normalization**: Proper table relationships with foreign keys
7. **NoSQL vs SQL**: Comparison of document-based and relational models
8. **ACID Properties**: Transaction management in PostgreSQL
9. **Eventual Consistency**: MongoDB's consistency model
10. **Role-Based Access Control (RBAC)**: Fine-grained permissions

## 🤝 Contributing

This is an educational project. Feel free to:
- Extend the schema with more tables/collections
- Add new federated query samples
- Improve the UI design
- Add data visualization features
- Implement caching mechanisms

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Apache Drill documentation: https://drill.apache.org/docs/
3. Check Flask documentation: https://flask.palletsprojects.com/
4. Review PostgreSQL/MongoDB docs for database-specific issues

## 🎉 Acknowledgments

- Apache Drill for federated query capabilities
- Flask framework for backend simplicity
- PostgreSQL and MongoDB communities
- Educational institutions supporting DBMS learning

---

**Happy Querying! 🚀**
#   d b m s e l _ s a a t h 
 
 
