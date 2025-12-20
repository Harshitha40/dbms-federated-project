# ========================================
# MongoDB Database Setup Instructions
# ========================================

# STEP 1: Start MongoDB Service
# Open PowerShell as Administrator and run:
net start MongoDB

# STEP 2: Connect to MongoDB Shell
# Open PowerShell and run:
mongosh

# STEP 3: Load the setup script
# From within mongosh, run:
load("c:/Users/Lenovo/dbmsel/proj/database/mongodb_setup.js")

# OR run from PowerShell directly:
# mongosh < database/mongodb_setup.js

# STEP 4: Verify the setup
# In mongosh:
use environmental_db
show collections
db.Biodiversity_Data.find().pretty()
db.Sensor_Logs.find().pretty()

# ========================================
# Connection Details
# ========================================
# Host: localhost
# Port: 27017
# Database: environmental_db
# No authentication required (default local setup)

# ========================================
# Collections Created
# ========================================
# 1. Biodiversity_Data - Species diversity information
# 2. Sensor_Logs - Real-time sensor events
# 3. Air_Quality_History - Historical air quality data
# 4. Species_Details - Detailed species information
# 5. Sensor_Metadata - Sensor device information
