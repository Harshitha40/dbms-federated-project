# ⚙️ SETUP CHECKLIST
## Pre-Launch Verification Guide

Use this checklist before running your application for the first time.

---

## 📋 STEP-BY-STEP SETUP CHECKLIST

### ✅ PHASE 1: Install Software (One-time setup)

- [ ] **Python 3.8+** installed
  - Test: `python --version`
  - Download: https://www.python.org/downloads/

- [ ] **Java 8+** installed (for Apache Drill)
  - Test: `java -version`
  - Download: https://adoptium.net/

- [ ] **PostgreSQL 12+** installed
  - Test: `psql --version`
  - Download: https://www.postgresql.org/download/

- [ ] **MongoDB 4.4+** installed
  - Test: `mongosh --version`
  - Download: https://www.mongodb.com/try/download/community

- [ ] **Apache Drill 1.20+** extracted
  - Location: Note your extraction path
  - Download: https://drill.apache.org/download/

---

### ✅ PHASE 2: Configure PostgreSQL

- [ ] PostgreSQL service is running
  ```powershell
  net start postgresql-x64-14
  ```

- [ ] You know your PostgreSQL password
  - Default user: `postgres`
  - Password: Set during installation

- [ ] Created environmental_db database
  ```sql
  psql -U postgres
  CREATE DATABASE environmental_db;
  \q
  ```

- [ ] Loaded schema and data
  ```sql
  psql -U postgres -d environmental_db
  \i C:/Users/Lenovo/dbmsel/proj/database/postgresql_schema.sql
  \dt
  -- Should show 5 tables
  \q
  ```

- [ ] Created a `.env` file from `.env.example` with `POSTGRES_PASSWORD=<your_postgres_password>`
  ```bash
  # Copy and edit
  copy .env.example .env
  # Edit .env and set POSTGRES_PASSWORD
  ```

- [ ] Verified data exists
  ```sql
  psql -U postgres -d environmental_db
  SELECT COUNT(*) FROM User_Info;
  -- Should return 3
  \q
  ```

---

### ✅ PHASE 3: Configure MongoDB

- [ ] MongoDB service is running
  ```powershell
  net start MongoDB
  ```

- [ ] Can connect to MongoDB
  ```powershell
  mongosh
  -- Should connect successfully
  exit
  ```

- [ ] Loaded MongoDB data
  ```javascript
  mongosh
  load("C:/Users/Lenovo/dbmsel/proj/database/mongodb_setup.js")
  -- Should see success message
  exit
  ```

- [ ] Verified collections exist
  ```javascript
  mongosh
  use environmental_db
  show collections
  -- Should show 5 collections
  exit
  ```

---

### ✅ PHASE 4: Configure Apache Drill

- [ ] Apache Drill is running
  ```powershell
  cd C:\drill\apache-drill-x.xx.x
  bin\drill-embedded.bat
  -- Keep this window open!
  ```

- [ ] Can access Drill Web UI
  - Browser: http://localhost:8047
  - Should load without errors

- [ ] Downloaded PostgreSQL JDBC driver
  - File: `postgresql-42.7.1.jar`
  - Download: https://jdbc.postgresql.org/download/

- [ ] Placed JDBC driver in correct location
  - Path: `C:\drill\apache-drill-x.xx.x\jars\3rdparty\postgresql-42.7.1.jar`
  - Created `3rdparty` folder if needed

- [ ] Restarted Drill after adding driver
  - Close Drill terminal
  - Run `bin\drill-embedded.bat` again

- [ ] Configured PostgreSQL storage plugin
  - Go to: http://localhost:8047/storage
  - Update `postgres` plugin with your password
  - Click "Update"
  - Enabled: ✓

- [ ] Configured MongoDB storage plugin
  - Go to: http://localhost:8047/storage
  - Update `mongo` plugin
  - Click "Update"
  - Enabled: ✓

- [ ] Configured DFS (CSV) storage plugin
  - Go to: http://localhost:8047/storage
  - Update `dfs` plugin
  - Added `data` workspace pointing to: `C:/Users/Lenovo/dbmsel/proj/data`
  - Click "Update"
  - Enabled: ✓

- [ ] Tested PostgreSQL connection in Drill
  ```sql
  SELECT * FROM postgres.public.`Region_Info` LIMIT 3;
  -- Should return 3 rows
  ```

- [ ] Tested MongoDB connection in Drill
  ```sql
  SELECT * FROM mongo.environmental_db.`Biodiversity_Data` LIMIT 3;
  -- Should return 3 rows
  ```

- [ ] Tested CSV file connection in Drill
  ```sql
  SELECT * FROM dfs.data.`sensor_readings.csv` LIMIT 3;
  -- Should return 3 rows
  ```

---

### ✅ PHASE 5: Setup Flask Backend

- [ ] Installed Python dependencies
  ```powershell
  cd C:\Users\Lenovo\dbmsel\proj\backend
  pip install -r requirements.txt
  ```

- [ ] Verified all packages installed
  ```powershell
  pip list | findstr "Flask psycopg2 pymongo bcrypt requests"
  -- Should show all packages
  ```

- [ ] Created `.env` and restarted backend with the new credentials
  - File: `.env` (created from `.env.example`)
  - Ensure `POSTGRES_PASSWORD` is set and then restart Flask server

- [ ] Started Flask server
  ```powershell
  cd C:\Users\Lenovo\dbmsel\proj\backend
  python app.py
  ```

- [ ] Verified all database connections
  ```
  PostgreSQL: ✓ Connected
  MongoDB: ✓ Connected
  Apache Drill: ✓ Connected
  ```

- [ ] Server is running on port 5000
  ```
  * Running on http://0.0.0.0:5000
  ```

---

### ✅ PHASE 6: Test the Application

- [ ] Can access login page
  - Browser: http://localhost:5000
  - Should show login form

- [ ] Can login as Researcher
  - Email: `sarah.researcher@example.com`
  - Password: `password123`
  - Should redirect to dashboard

- [ ] Can access query interface
  - Click "Open Query Interface"
  - Should load query page

- [ ] Can execute a test query
  ```sql
  SELECT * FROM postgres.public.`Region_Info` LIMIT 5;
  ```
  - Should return 5 rows in table

- [ ] Can logout and login as different role
  - Logout
  - Login as: `mike.provider@example.com`
  - Should see different dashboard

- [ ] Can insert data (as Data Provider)
  - Go to "Manage Data"
  - Fill climate data form
  - Submit - should see success message

- [ ] Can access admin panel (as Administrator)
  - Logout and login as: `admin@example.com`
  - Go to "Admin Panel"
  - Should see user list

---

## 🎯 QUICK VERIFICATION SCRIPT

Run this PowerShell script to check everything at once:

```powershell
Write-Host "=== FEDERATED DBMS SETUP VERIFICATION ===" -ForegroundColor Cyan

# Check Python
Write-Host "`n1. Checking Python..." -ForegroundColor Yellow
python --version

# Check Java
Write-Host "`n2. Checking Java..." -ForegroundColor Yellow
java -version

# Check PostgreSQL
Write-Host "`n3. Checking PostgreSQL..." -ForegroundColor Yellow
psql --version

# Check MongoDB
Write-Host "`n4. Checking MongoDB..." -ForegroundColor Yellow
mongosh --version

# Check if PostgreSQL is running
Write-Host "`n5. Checking PostgreSQL service..." -ForegroundColor Yellow
sc query postgresql-x64-14

# Check if MongoDB is running
Write-Host "`n6. Checking MongoDB service..." -ForegroundColor Yellow
sc query MongoDB

# Check if Drill Web UI is accessible
Write-Host "`n7. Checking Apache Drill..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8047" -TimeoutSec 5
    Write-Host "Apache Drill is running!" -ForegroundColor Green
} catch {
    Write-Host "Apache Drill is NOT running!" -ForegroundColor Red
}

# Check if Flask is running
Write-Host "`n8. Checking Flask Backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -TimeoutSec 5
    Write-Host "Flask backend is running!" -ForegroundColor Green
} catch {
    Write-Host "Flask backend is NOT running!" -ForegroundColor Red
}

Write-Host "`n=== VERIFICATION COMPLETE ===" -ForegroundColor Cyan
```

Save this as `check_setup.ps1` and run: `.\check_setup.ps1`

---

## 🔧 Common Issues Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Can't connect to PostgreSQL | `net start postgresql-x64-14` |
| Can't connect to MongoDB | `net start MongoDB` |
| Drill not responding | Restart: `bin\drill-embedded.bat` |
| JDBC driver not found | Download and place in `jars/3rdparty/`, restart Drill |
| Password authentication failed | Update `backend/config.py` with correct password |
| Port 5000 in use | Close other Flask apps or change port in `app.py` |
| Table not found in Drill | Use backticks: \`table_name\` |
| Storage plugin disabled | Go to Drill Web UI → Storage → Enable plugin |

---

## 📞 Need Help?

### If something doesn't work:

1. **Read the error message** carefully
2. **Check the relevant guide:**
   - Connection issues → `CONNECTION_GUIDE.md`
   - Quick setup → `QUICKSTART.md`
   - Drill issues → `config/drill_setup.md`
   - Full details → `README.md`

3. **Restart everything:**
   ```powershell
   # Stop all
   net stop postgresql-x64-14
   net stop MongoDB
   # Close Drill terminal
   # Close Flask terminal
   
   # Start all
   net start postgresql-x64-14
   net start MongoDB
   # Start Drill: bin\drill-embedded.bat
   # Start Flask: python app.py
   ```

4. **Verify step by step** using this checklist

---

## ✨ Success Indicators

You'll know everything is working when:

✅ All 3 databases show "Connected" when Flask starts
✅ You can login to the web application
✅ You can execute a federated query successfully
✅ Query results display in a table
✅ No red error messages appear

---

## 🎉 All Done?

If you checked all boxes above, you're ready to:
- Execute federated queries
- Insert data across databases
- Explore the admin panel
- Test different user roles
- Learn about federated DBMS!

**Congratulations! Your Federated DBMS is ready! 🚀**
