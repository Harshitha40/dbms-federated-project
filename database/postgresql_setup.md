# ========================================
# PostgreSQL Database Setup Instructions
# ========================================

# STEP 1: Connect to PostgreSQL
# Open PowerShell and connect to PostgreSQL using psql:
# psql -U postgres

# STEP 2: Create Database
# Run this in psql prompt:
CREATE DATABASE environmental_db;

# STEP 3: Connect to the database
# \c environmental_db

# STEP 4: Run the schema file
# Exit psql and run from PowerShell:
# psql -U postgres -d environmental_db -f database/postgresql_schema.sql

# OR from within psql:
# \i c:/Users/Lenovo/dbmsel/proj/database/postgresql_schema.sql

# STEP 5: Verify the setup
# psql -U postgres -d environmental_db
# \dt  (list all tables)
# SELECT * FROM User_Info;

# ========================================
# Default Credentials
# ========================================
# Username: postgres
# Password: (your PostgreSQL installation password)
# Database: environmental_db
# Port: 5432
# Host: localhost

# ========================================
# Test Login Credentials (password: 'password123')
# ========================================
# Researcher: sarah.researcher@example.com
# Data Provider: mike.provider@example.com
# Administrator: admin@example.com
