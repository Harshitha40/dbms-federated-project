# 🚀 QUICK START GUIDE
### Federated Environmental Intelligence Platform

## ⚡ Super Fast Setup (15 minutes)

### 1. Check Prerequisites (2 min)

Open PowerShell and verify:

```powershell
# Check Python
python --version

# Check Java (for Drill)
java -version

# Check PostgreSQL
psql --version

# Check MongoDB
mongosh --version
```

If any are missing, install them first (see main README).

---

### 2. Setup Databases (5 min)

#### PostgreSQL
```powershell
# Start PostgreSQL
net start postgresql-x64-14

# Create database and load schema
psql -U postgres
```

In psql:
```sql
CREATE DATABASE environmental_db;
\c environmental_db
\i C:/Users/Lenovo/dbmsel/proj/database/postgresql_schema.sql
\q
```

**⚠️ IMPORTANT:** Edit `backend/config.py` and change PostgreSQL password!

#### MongoDB
```powershell
# Start MongoDB
net start MongoDB

# Load data
mongosh
```

In mongosh:
```javascript
load("C:/Users/Lenovo/dbmsel/proj/database/mongodb_setup.js")
exit
```

---

### 3. Setup Apache Drill (5 min)

```powershell
# Start Drill
cd C:\drill\apache-drill-x.xx.x
bin\drill-embedded.bat
```

**Open browser:** http://localhost:8047

**Configure 3 storage plugins:**

1. **Storage → postgres → Update:**
```json
{
  "type": "jdbc",
  "driver": "org.postgresql.Driver",
  "url": "jdbc:postgresql://localhost:5432/environmental_db",
  "username": "postgres",
  "password": "YOUR_POSTGRES_PASSWORD",
  "enabled": true
}
```

2. **Storage → mongo → Update:**
```json
{
  "type": "mongo",
  "connection": "mongodb://localhost:27017/",
  "enabled": true
}
```

3. **Storage → dfs → Update** (add this to workspaces section):
```json
"data": {
  "location": "C:/Users/Lenovo/dbmsel/proj/data",
  "writable": false,
  "defaultInputFormat": "csv"
}
```

**⚠️ Download PostgreSQL JDBC Driver:**
- Get: https://jdbc.postgresql.org/download/postgresql-42.7.1.jar
- Put in: `apache-drill/jars/3rdparty/`
- **Restart Drill** after adding the driver

**Test in Query tab:**
```sql
SELECT * FROM postgres.public.`Region_Info` LIMIT 3;
SELECT * FROM mongo.environmental_db.`Biodiversity_Data` LIMIT 3;
SELECT * FROM dfs.data.`sensor_readings.csv` LIMIT 3;
```

---

### 4. Install Python Dependencies (2 min)

```powershell
cd C:\Users\Lenovo\dbmsel\proj\backend
pip install -r requirements.txt
```

---

### 5. Start the Application (1 min)

```powershell
# Make sure you're in backend directory
cd C:\Users\Lenovo\dbmsel\proj\backend

# Run Flask app
python app.py
```

You should see:
```
PostgreSQL: ✓ Connected
MongoDB: ✓ Connected
Apache Drill: ✓ Connected
```

**Open browser:** http://localhost:5000

---

## 🎯 Test Login Credentials

**Researcher:**
- Email: `sarah.researcher@example.com`
- Password: `password123`

**Data Provider:**
- Email: `mike.provider@example.com`
- Password: `password123`

**Administrator:**
- Email: `admin@example.com`
- Password: `password123`

---

## ✅ Quick Test Checklist

After logging in as **Researcher**, try this federated query:

```sql
SELECT 
    r.region_name,
    c.temperature,
    c.rainfall
FROM postgres.public.`Region_Info` r
JOIN postgres.public.`Climate_Data` c ON r.region_id = c.region_id
LIMIT 5;
```

If you see results → **SUCCESS!** 🎉

---

## 🐛 Common Issues & Quick Fixes

### Issue: "PostgreSQL connection failed"
**Fix:** 
1. Edit `backend/config.py`
2. Change password to your actual PostgreSQL password
3. Restart Flask app

### Issue: "Drill connection failed"
**Fix:**
1. Check http://localhost:8047 is accessible
2. Verify PostgreSQL JDBC driver is in `jars/3rdparty/`
3. Restart Drill

### Issue: "Cannot find table"
**Fix:** Use backticks around table names:
```sql
-- Wrong
SELECT * FROM postgres.public.Region_Info

-- Correct
SELECT * FROM postgres.public.`Region_Info`
```

### Issue: "MongoDB connection failed"
**Fix:**
```powershell
net start MongoDB
mongosh  # Should connect without errors
```

### Issue: Flask won't start
**Fix:**
```powershell
# Make sure all dependencies installed
pip install Flask Flask-CORS psycopg2-binary pymongo bcrypt requests
```

---

## 📋 Services Checklist

Before running the app, ensure all services are running:

- [ ] PostgreSQL service started
- [ ] MongoDB service started
- [ ] Apache Drill running (http://localhost:8047 accessible)
- [ ] All 3 Drill storage plugins configured and enabled
- [ ] Flask backend running (python app.py)

---

## 🎓 What to Try First

1. **Login** as Researcher
2. **Go to** Federated Query page
3. **Click** a sample query
4. **Execute** the query
5. **View** results in table
6. **Try** joining data from different sources

Then:
- Login as Data Provider → Insert new data
- Login as Administrator → View query logs, create users

---

## 📚 Need More Help?

- **Full documentation:** See `README.md`
- **Sample queries:** See `config/sample_federated_queries.sql`
- **Drill setup:** See `config/drill_setup.md`
- **Database setup:** See files in `database/` folder

---

## 💡 Pro Tips

1. **Test each database connection separately first** before running federated queries
2. **Start with simple queries** before trying complex joins
3. **Use LIMIT clause** when testing queries on large datasets
4. **Check Drill Web UI** (http://localhost:8047) to verify storage plugins
5. **Keep browser console open** (F12) to see any JavaScript errors

---

**Ready to explore federated databases? Let's go! 🚀**
