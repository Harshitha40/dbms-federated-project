# 🔌 DATABASE CONNECTION GUIDE FOR BEGINNERS
### Step-by-Step Guide to Connect PostgreSQL, MongoDB, and Apache Drill

This guide explains exactly how to connect your databases. Follow each step carefully.

---

## 📖 Table of Contents
1. [Understanding Database Connections](#understanding-database-connections)
2. [PostgreSQL Connection](#postgresql-connection)
3. [MongoDB Connection](#mongodb-connection)
4. [Apache Drill Setup](#apache-drill-setup)
5. [Testing Connections](#testing-connections)
6. [Common Connection Problems](#common-connection-problems)

---

## 🎓 Understanding Database Connections

### What is a Database Connection?

A **database connection** is like making a phone call to a database:
- You need the **phone number** (host and port)
- You need **authentication** (username and password)
- Once connected, you can **send commands** and **receive data**

### Connection Components:

```
┌─────────────────────────────────────┐
│        Your Application             │
│         (Flask Backend)             │
└───────────┬─────────────────────────┘
            │
            │ Connection String
            │ (Host + Port + Credentials)
            │
┌───────────▼─────────────────────────┐
│         Database Server             │
│    (PostgreSQL/MongoDB/Drill)       │
└─────────────────────────────────────┘
```

---

## 🐘 PostgreSQL Connection

### Step 1: Find Your PostgreSQL Password

During PostgreSQL installation, you set a password for the `postgres` user. You'll need this password.

**If you forgot your password:**
1. Open `pgAdmin` (installed with PostgreSQL)
2. Or reset password by reinstalling PostgreSQL

### Step 2: Test PostgreSQL Connection

Open PowerShell:

```powershell
# Try to connect
psql -U postgres

# If it asks for password, enter it
# If successful, you'll see: postgres=#
```

**Success looks like:**
```
Password for user postgres: [enter your password]
psql (14.x)
Type "help" for help.

postgres=#
```

Type `\q` to exit.

### Step 3: Configure Backend Connection

Open `backend/config.py` in a text editor (Notepad, VS Code, etc.):

Find this section:
```python
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'environmental_db',
    'user': 'postgres',
    'password': 'postgres'  # ← CHANGE THIS LINE
}
```

Change `'postgres'` to your actual password:
```python
    'password': 'your_actual_password_here'  # ← Your password
```

**Example:**
If your password is `mypassword123`, change it to:
```python
    'password': 'mypassword123'
```

Save the file.

### Step 4: Create the Database

```powershell
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE environmental_db;

# Connect to the new database
\c environmental_db

# You should see: You are now connected to database "environmental_db"

# Load the schema (creates tables and data)
\i C:/Users/Lenovo/dbmsel/proj/database/postgresql_schema.sql

# Check if tables were created
\dt

# You should see a list of 5 tables
# Exit
\q
```

---

## 🍃 MongoDB Connection

### Step 1: Check if MongoDB is Running

```powershell
# Check MongoDB service status
sc query MongoDB

# If stopped, start it:
net start MongoDB
```

### Step 2: Test MongoDB Connection

```powershell
# Try to connect using mongosh
mongosh

# If successful, you'll see:
# Connecting to: mongodb://localhost:27017
# Current Mongosh Log ID: xxxxx
# Using MongoDB: x.x.x
```

Type `exit` to quit.

### Step 3: Load Sample Data

```powershell
# Connect to MongoDB
mongosh

# Load the setup script
load("C:/Users/Lenovo/dbmsel/proj/database/mongodb_setup.js")

# You should see:
# MongoDB collections created successfully!
# Total documents:
# - Biodiversity_Data: 4
# - Sensor_Logs: 5
# ...etc

# Verify
use environmental_db
show collections

# You should see 5 collections listed

# Exit
exit
```

### Step 4: Backend Configuration

The MongoDB configuration in `backend/config.py` should already work:

```python
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'environmental_db'
}
```

**No password needed** for local MongoDB (default installation).

---

## 🔧 Apache Drill Setup

Apache Drill is the most complex part. Follow these steps carefully.

### Step 1: Verify Java Installation

Drill needs Java to run.

```powershell
# Check Java version
java -version

# You should see:
# openjdk version "1.8.x" or higher
```

**If Java is not installed:**
1. Download from: https://adoptium.net/
2. Install Java 8 or later
3. Restart PowerShell

### Step 2: Find Your Drill Installation

Drill should be extracted somewhere like:
- `C:\drill\apache-drill-1.21.0`
- `C:\Program Files\apache-drill-1.21.0`
- Or wherever you extracted it

**Navigate to your Drill folder:**
```powershell
# Example (adjust to your path)
cd C:\drill\apache-drill-1.21.0
```

### Step 3: Start Apache Drill

```powershell
# From your Drill directory
bin\drill-embedded.bat

# You should see:
# Apache Drill 1.x.x
# ...
# Drill log directory is: ...
# Starting Drill in embedded mode...
```

**Keep this window open!** Drill runs in this terminal window.

### Step 4: Access Drill Web UI

Open your web browser and go to:
```
http://localhost:8047
```

You should see the Apache Drill web interface.

### Step 5: Download PostgreSQL JDBC Driver

This is REQUIRED for Drill to connect to PostgreSQL.

1. **Go to:** https://jdbc.postgresql.org/download/
2. **Download:** `postgresql-42.7.1.jar` (or latest version)
3. **Save to:** `C:\drill\apache-drill-x.xx.x\jars\3rdparty\`
   - Create the `3rdparty` folder if it doesn't exist

**Example file location:**
```
C:\drill\apache-drill-1.21.0\jars\3rdparty\postgresql-42.7.1.jar
```

4. **Restart Drill:**
   - Close the Drill terminal window
   - Run `bin\drill-embedded.bat` again

### Step 6: Configure Storage Plugins

In the Drill Web UI (http://localhost:8047):

#### A. Configure PostgreSQL Plugin

1. Click **"Storage"** tab at the top
2. Find **"cp"** or create a new plugin called **"postgres"**
3. Click **"Update"**
4. Replace the configuration with:

```json
{
  "type": "jdbc",
  "driver": "org.postgresql.Driver",
  "url": "jdbc:postgresql://localhost:5432/environmental_db",
  "username": "postgres",
  "password": "YOUR_POSTGRES_PASSWORD_HERE",
  "enabled": true
}
```

**⚠️ Replace `YOUR_POSTGRES_PASSWORD_HERE` with your actual PostgreSQL password!**

5. Click **"Update"** button
6. You should see: "Successfully updated"

#### B. Configure MongoDB Plugin

1. Still in **"Storage"** tab
2. Find **"mongo"** plugin
3. Click **"Update"**
4. Replace with:

```json
{
  "type": "mongo",
  "connection": "mongodb://localhost:27017/",
  "enabled": true
}
```

5. Click **"Update"**

#### C. Configure CSV File Plugin (DFS)

1. Find **"dfs"** plugin
2. Click **"Update"**
3. Find the **"workspaces"** section
4. Add this workspace (inside the workspaces object):

```json
"data": {
  "location": "C:/Users/Lenovo/dbmsel/proj/data",
  "writable": false,
  "defaultInputFormat": "csv"
}
```

**Complete example** (your dfs config should look similar):
```json
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
```

5. Click **"Update"**

---

## ✅ Testing Connections

### Test in Drill Web UI

Go to **"Query"** tab in Drill (http://localhost:8047):

**Test 1: PostgreSQL**
```sql
SELECT * FROM postgres.public.`Region_Info` LIMIT 3;
```

Expected: You should see 3 rows with region data

**Test 2: MongoDB**
```sql
SELECT * FROM mongo.environmental_db.`Biodiversity_Data` LIMIT 3;
```

Expected: You should see 3 rows with biodiversity data

**Test 3: CSV File**
```sql
SELECT * FROM dfs.data.`sensor_readings.csv` LIMIT 3;
```

Expected: You should see 3 rows with sensor readings

**If all 3 work → Your Drill is configured correctly! 🎉**

### Test Flask Backend

```powershell
# Navigate to backend folder
cd C:\Users\Lenovo\dbmsel\proj\backend

# Run the Flask app
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
```

**If you see all ✓ Connected → Everything is working!**

---

## 🐛 Common Connection Problems

### Problem 1: PostgreSQL "password authentication failed"

**Cause:** Wrong password in `config.py`

**Fix:**
1. Open `backend/config.py`
2. Change the password to your actual PostgreSQL password
3. Save and restart Flask

### Problem 2: MongoDB "connection refused"

**Cause:** MongoDB service not running

**Fix:**
```powershell
net start MongoDB
```

### Problem 3: Drill "table not found"

**Cause:** Storage plugin not configured or not enabled

**Fix:**
1. Go to http://localhost:8047/storage
2. Check if plugin shows **"enabled": true**
3. Click "Enable" if it's disabled
4. Retry your query

### Problem 4: Drill "JDBC driver not found"

**Cause:** PostgreSQL JDBC driver not installed

**Fix:**
1. Download `postgresql-42.7.1.jar`
2. Copy to `apache-drill/jars/3rdparty/`
3. **Restart Drill completely**

### Problem 5: "Port already in use"

**Cause:** Service already running or port blocked

**Fix:**
- PostgreSQL (port 5432): Stop and restart the service
- MongoDB (port 27017): Stop and restart the service
- Drill (port 8047): Close the Drill terminal and restart
- Flask (port 5000): Close the Flask terminal and restart

### Problem 6: Can't connect from browser

**Cause:** Flask not running or wrong URL

**Fix:**
1. Make sure Flask is running: `python app.py`
2. Use correct URL: http://localhost:5000
3. Check browser console (F12) for errors

---

## 🎯 Connection Checklist

Before running the application, verify:

- [ ] PostgreSQL service is running
- [ ] PostgreSQL password is correct in `config.py`
- [ ] Database `environmental_db` exists in PostgreSQL
- [ ] Tables are created (5 tables)
- [ ] MongoDB service is running
- [ ] MongoDB collections are created (5 collections)
- [ ] Apache Drill is running
- [ ] PostgreSQL JDBC driver is in `jars/3rdparty/`
- [ ] All 3 Drill storage plugins are configured and enabled
- [ ] Test queries work in Drill Web UI
- [ ] Flask backend shows all connections successful

---

## 💡 Understanding Connection Strings

### PostgreSQL Connection String Format:
```
postgresql://username:password@host:port/database
```

Example:
```
postgresql://postgres:mypassword@localhost:5432/environmental_db
```

### MongoDB Connection String Format:
```
mongodb://host:port/database
```

Example:
```
mongodb://localhost:27017/environmental_db
```

### Apache Drill REST API Format:
```
http://host:port/query.json
```

Example:
```
http://localhost:8047/query.json
```

---

## 🔐 Security Note

**For this educational project:**
- Passwords are stored in `config.py`
- MongoDB has no authentication (local development only)
- This is OK for learning!

**For production:**
- Use environment variables for passwords
- Enable MongoDB authentication
- Use SSL/TLS connections
- Never commit passwords to Git

---

## 🆘 Still Having Issues?

1. **Check Service Status:**
```powershell
# PostgreSQL
sc query postgresql-x64-14

# MongoDB
sc query MongoDB
```

2. **Check Ports:**
```powershell
# See what's using ports
netstat -ano | findstr "5432"  # PostgreSQL
netstat -ano | findstr "27017" # MongoDB
netstat -ano | findstr "8047"  # Drill
netstat -ano | findstr "5000"  # Flask
```

3. **Restart Everything:**
```powershell
# Stop all services
net stop postgresql-x64-14
net stop MongoDB
# Close Drill terminal
# Close Flask terminal

# Start again
net start postgresql-x64-14
net start MongoDB
# Start Drill: bin\drill-embedded.bat
# Start Flask: python app.py
```

---

**You're ready to connect! 🚀**
