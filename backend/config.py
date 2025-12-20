# ========================================
# Database Configuration
# ========================================

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# PostgreSQL Configuration
POSTGRES_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
    'database': os.getenv('POSTGRES_DB', 'environmental_db'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD')
}

# MongoDB Configuration
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'environmental_db',
    'uri': os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
}

# Apache Drill Configuration
DRILL_CONFIG = {
    'host': os.getenv('DRILL_HOST', 'localhost'),
    'port': int(os.getenv('DRILL_PORT', 8047))
}

# Flask Configuration
SECRET_KEY = 'your-secret-key-change-this-in-production'  # CHANGE THIS in production
SESSION_TYPE = 'filesystem'
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

# Groq Configuration (for LLM-powered natural language queries)
# Get your API key from: https://console.groq.com/keys
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# CSV Data Path
CSV_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sensor_readings.csv')
