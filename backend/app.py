# ========================================
# FEDERATED ENVIRONMENTAL INTELLIGENCE PLATFORM
# Flask Backend Server
# ========================================

from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

# Import our modules
from config import SECRET_KEY, SESSION_TYPE, PERMANENT_SESSION_LIFETIME
from database import db_manager
from auth import (
    authenticate_user, create_user_session, destroy_user_session,
    get_current_user, login_required, role_required,
    get_all_users, create_new_user, delete_user,
    log_query, get_query_logs
)
from llm_query import LLMQueryConverter

# ========================================
# Flask App Initialization
# ========================================
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = SECRET_KEY
app.config['SESSION_TYPE'] = SESSION_TYPE
app.config['PERMANENT_SESSION_LIFETIME'] = PERMANENT_SESSION_LIFETIME

# Enable CORS for frontend communication
CORS(app, supports_credentials=True)

# ========================================
# Static File Serving
# ========================================
@app.route('/')
def index():
    """Serve the login page as default"""
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (HTML, CSS, JS)"""
    return send_from_directory(app.static_folder, path)

# ========================================
# Authentication Routes
# ========================================
@app.route('/api/login', methods=['POST'])
def login():
    """
    User login endpoint.
    Expects JSON: {"email": "user@example.com", "password": "password123"}
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Authenticate user
        user = authenticate_user(email, password)

        # Handle DB availability case
        if isinstance(user, dict) and user.get('_db_error'):
            return jsonify({
                'success': False,
                'error': 'Database unavailable. Please check PostgreSQL configuration.'
            }), 500
        
        if user:
            # Create session
            create_user_session(user)
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Login error: {str(e)}'
        }), 500


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """User logout endpoint"""
    try:
        destroy_user_session()
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Logout error: {str(e)}'
        }), 500


@app.route('/api/current-user', methods=['GET'])
@login_required
def current_user():
    """Get current logged-in user information"""
    user = get_current_user()
    return jsonify({
        'success': True,
        'user': user
    }), 200


# ========================================
# Database Status Routes
# ========================================
@app.route('/api/database-status', methods=['GET'])
@login_required
def database_status():
    """
    Check status of all database connections.
    Useful for monitoring and debugging.
    """
    try:
        status = {
            'postgres': db_manager.postgres.test_connection(),
            'mongodb': db_manager.mongo.test_connection(),
            'drill': db_manager.drill.test_connection()
        }
        
        return jsonify({
            'success': True,
            'status': status
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========================================
# Federated Query Routes (Researcher & Admin)
# ========================================
@app.route('/api/federated-query', methods=['POST'])
@role_required('Researcher', 'Administrator')
def federated_query():
    """
    Execute a federated query using Apache Drill.
    Expects JSON: {"query": "SELECT * FROM ..."}
    """
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        # Get current user
        user = get_current_user()
        
        # Execute query through Drill
        result = db_manager.drill.execute_query(query)
        
        # Log the query
        log_query(user['user_id'], query)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['rows'],
                'columns': result['columns']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Query execution failed')
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Query error: {str(e)}'
        }), 500



@app.route('/api/sample-queries', methods=['GET'])
@role_required('Researcher', 'Administrator')
def sample_queries():
    """
    Get sample federated queries for users.
    Helps users understand federated query syntax.
    """
    samples = [
        {
            'name': 'All Regions',
            'description': 'List all environmental regions',
            'query': 'SELECT * FROM postgres.public.`region_info` LIMIT 10'
        },
        {
            'name': 'Climate Data',
            'description': 'Recent climate measurements',
            'query': 'SELECT * FROM postgres.public.`climate_data` LIMIT 10'
        },
        {
            'name': 'Biodiversity Info',
            'description': 'Species diversity data from MongoDB',
            'query': 'SELECT * FROM mongo.environmental_db.`Biodiversity_Data` LIMIT 10'
        },
        {
            'name': 'Sensor Readings',
            'description': 'Real-time sensor data from CSV',
            'query': 'SELECT * FROM dfs.data.`sensor_readings.csv` LIMIT 10'
        },
        {
            'name': 'Agriculture Data',
            'description': 'Crop yields by region',
            'query': 'SELECT * FROM postgres.public.`agriculture_data` LIMIT 10'
        },
        {
            'name': 'Air Quality History',
            'description': 'Historical air quality from MongoDB',
            'query': 'SELECT * FROM mongo.environmental_db.`Air_Quality_History` LIMIT 5'
        },
        {
            'name': 'Regions with Climate',
            'description': 'Join PostgreSQL tables: regions + climate',
            'query': '''SELECT 
                r.region_name, 
                r.latitude,
                r.longitude,
                c.temperature, 
                c.rainfall,
                c.humidity
            FROM postgres.public.`climate_data` c
            JOIN postgres.public.`region_info` r ON c.region_id = r.region_id
            LIMIT 10'''
        },
        {
            'name': 'Regions with Agriculture',
            'description': 'Join PostgreSQL: regions + crop yields',
            'query': '''SELECT 
                r.region_name,
                a.crop_type,
                a.yield,
                a.season,
                a.year
            FROM postgres.public.`agriculture_data` a
            JOIN postgres.public.`region_info` r ON a.region_id = r.region_id
            LIMIT 10'''
        },
        {
            'name': 'Climate vs Biodiversity',
            'description': 'Federated join: PostgreSQL + MongoDB',
            'query': '''WITH 
                pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
                pg_climate AS (SELECT region_id, temperature, humidity FROM postgres.public.`climate_data`),
                mongo_bio AS (SELECT region_id, species_count, conservation_status FROM mongo.environmental_db.`Biodiversity_Data`)
            SELECT 
                r.region_name,
                c.temperature,
                c.humidity,
                b.species_count,
                b.conservation_status
            FROM pg_region r
            JOIN pg_climate c ON r.region_id = c.region_id
            JOIN mongo_bio b ON r.region_id = b.region_id
            LIMIT 50'''
        },
        {
            'name': 'Sensors vs Climate',
            'description': 'Federated join: CSV + PostgreSQL',
            'query': '''WITH 
                csv_sensors AS (SELECT CAST(region_id AS INT) as rid, CAST(co2_level AS FLOAT) as co2, CAST(pm2_5 AS FLOAT) as pm FROM dfs.data.`sensor_readings.csv`),
                pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
                pg_climate AS (SELECT region_id, temperature, humidity FROM postgres.public.`climate_data`)
            SELECT 
                r.region_name,
                s.co2 as co2_level,
                s.pm as pm2_5,
                c.temperature,
                c.humidity
            FROM csv_sensors s
            JOIN pg_region r ON s.rid = r.region_id
            JOIN pg_climate c ON r.region_id = c.region_id
            LIMIT 50'''
        },
        {
            'name': 'Complete Environmental View',
            'description': 'Join PostgreSQL (3 tables) + MongoDB',
            'query': '''WITH 
                pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
                pg_climate AS (SELECT region_id, temperature, rainfall FROM postgres.public.`climate_data`),
                pg_agri AS (SELECT region_id, crop_type, `yield` as crop_yield FROM postgres.public.`agriculture_data`),
                mongo_bio AS (SELECT region_id, species_count FROM mongo.environmental_db.`Biodiversity_Data`)
            SELECT 
                r.region_name,
                c.temperature,
                c.rainfall,
                a.crop_type,
                a.crop_yield,
                b.species_count
            FROM pg_region r
            LEFT JOIN pg_climate c ON r.region_id = c.region_id
            LEFT JOIN pg_agri a ON r.region_id = a.region_id
            LEFT JOIN mongo_bio b ON r.region_id = b.region_id
            LIMIT 50'''
        },
        {
            'name': 'High Temp Regions with Species',
            'description': 'Filter + join: Hot regions with biodiversity',
            'query': '''WITH 
                pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
                pg_climate AS (SELECT region_id, temperature FROM postgres.public.`climate_data`),
                mongo_bio AS (SELECT region_id, species_count, conservation_status FROM mongo.environmental_db.`Biodiversity_Data`)
            SELECT 
                r.region_name,
                c.temperature,
                b.species_count,
                b.conservation_status
            FROM pg_climate c
            JOIN pg_region r ON c.region_id = r.region_id
            JOIN mongo_bio b ON r.region_id = b.region_id
            WHERE c.temperature > 25
            LIMIT 50'''
        },
        {
            'name': 'High CO2 Regions Analysis',
            'description': 'CSV sensors + PostgreSQL regions',
            'query': '''WITH 
                csv_sensors AS (SELECT CAST(region_id AS INT) as rid, CAST(co2_level AS FLOAT) as co2, CAST(pm2_5 AS FLOAT) as pm FROM dfs.data.`sensor_readings.csv`),
                pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`)
            SELECT 
                r.region_name,
                AVG(s.co2) as avg_co2,
                AVG(s.pm) as avg_pm25,
                COUNT(*) as reading_count
            FROM csv_sensors s
            JOIN pg_region r ON s.rid = r.region_id
            GROUP BY r.region_name
            HAVING AVG(s.co2) > 420
            LIMIT 50'''
        },
        {
            'name': 'Critical Conservation Regions',
            'description': 'MongoDB + PostgreSQL: endangered species areas',
            'query': '''SELECT 
                r.region_name,
                r.latitude,
                r.longitude,
                b.species_count,
                b.conservation_status
            FROM mongo.environmental_db.`Biodiversity_Data` b
            JOIN postgres.public.`region_info` r ON b.region_id = r.region_id
            WHERE b.conservation_status = 'Critical'
            LIMIT 50'''
        },
        {
            'name': 'Top Crop Producing Regions',
            'description': 'Aggregate agriculture data by region',
            'query': '''SELECT 
                r.region_name,
                SUM(a.yield) as total_yield,
                COUNT(DISTINCT a.crop_type) as crop_diversity
            FROM postgres.public.`agriculture_data` a
            JOIN postgres.public.`region_info` r ON a.region_id = r.region_id
            GROUP BY r.region_name
            LIMIT 50'''
        }
    ]
    
    return jsonify({
        'success': True,
        'queries': samples
    }), 200


@app.route('/api/natural-query', methods=['POST'])
@role_required('Researcher', 'Administrator', 'Data Provider')
def natural_query():
    """
    Convert natural language query to SQL and execute it.
    Expects JSON: {"query": "show all regions with high temperature"}
    """
    try:
        data = request.get_json()
        natural_query = data.get('query', '').strip()
        
        if not natural_query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        # Initialize LLM converter
        converter = LLMQueryConverter()
        
        # Check if LLM is available
        use_llm = converter.is_available()
        
        # Convert natural language to SQL
        result = converter.convert(natural_query, use_llm=use_llm)
        sql_query = result['sql']
        confidence = result['confidence']
        interpretation = result['interpretation']
        method = result.get('method', 'pattern')
        
        print(f"\n{'='*60}")
        print(f"Natural Query: {natural_query}")
        print(f"Generated SQL: {sql_query}")
        print(f"Method: {method}, Confidence: {confidence}")
        print(f"{'='*60}\n")
        
        # Execute the generated SQL
        user = get_current_user()
        query_result = db_manager.drill.execute_query(sql_query)
        
        print(f"Query Result Success: {query_result['success']}")
        print(f"Rows returned: {len(query_result.get('rows', []))}")
        if not query_result['success']:
            print(f"Error: {query_result.get('error', 'Unknown')}")
        
        # Log the query
        log_query(user['user_id'], f"[NL: {natural_query}] {sql_query}")
        
        if query_result['success']:
            return jsonify({
                'success': True,
                'data': query_result['rows'],
                'columns': query_result['columns'],
                'generated_sql': sql_query,
                'confidence': confidence,
                'interpretation': interpretation,
                'natural_query': natural_query,
                'method': method,
                'llm_available': use_llm
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': query_result.get('error', 'Query execution failed'),
                'generated_sql': sql_query,
                'confidence': confidence,
                'interpretation': interpretation
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Natural language processing error: {str(e)}'
        }), 500


# ========================================
# Data Provider Routes (Insert/Update Only)
# ========================================
@app.route('/api/insert-climate', methods=['POST'])
@role_required('Data Provider', 'Administrator')
def insert_climate():
    """
    Insert new climate data.
    Expects JSON: {"region_id": 1, "temperature": 25.5, "rainfall": 100.0, "humidity": 80.0}
    """
    try:
        data = request.get_json()
        
        required_fields = ['region_id', 'temperature', 'rainfall', 'humidity']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        query = """
            INSERT INTO climate_data (region_id, temperature, rainfall, humidity)
            VALUES (%s, %s, %s, %s)
        """
        
        success = db_manager.postgres.execute_update(
            query,
            (data['region_id'], data['temperature'], data['rainfall'], data['humidity'])
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Climate data inserted successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to insert climate data'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Insert error: {str(e)}'
        }), 500


@app.route('/api/insert-agriculture', methods=['POST'])
@role_required('Data Provider', 'Administrator')
def insert_agriculture():
    """
    Insert new agriculture data.
    Expects JSON: {"region_id": 1, "crop_type": "Wheat", "yield": 45.2, "season": "Summer", "year": 2024}
    """
    try:
        data = request.get_json()
        
        required_fields = ['region_id', 'crop_type', 'yield', 'season', 'year']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        query = """
            INSERT INTO agriculture_data (region_id, crop_type, yield, season, year)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        success = db_manager.postgres.execute_update(
            query,
            (data['region_id'], data['crop_type'], data['yield'], data['season'], data['year'])
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Agriculture data inserted successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to insert agriculture data'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Insert error: {str(e)}'
        }), 500


@app.route('/api/insert-sensor-log', methods=['POST'])
@role_required('Data Provider', 'Administrator')
def insert_sensor_log():
    try:
        data = request.get_json()
        required_fields = ['sensor_id', 'region_id', 'event_type', 'severity', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        data['timestamp'] = datetime.utcnow()
        result = db_manager.mongo.insert_one('Sensor_Logs', data)
        if result:
            return jsonify({'success': True, 'message': 'Sensor log inserted successfully', 'id': str(result)}), 201
        return jsonify({'success': False, 'error': 'Failed to insert sensor log'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/insert-region', methods=['POST'])
@role_required('Data Provider', 'Administrator')
def insert_region():
    try:
        data = request.get_json()
        required = ['region_name', 'latitude', 'longitude']
        for field in required:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        query = "INSERT INTO region_info (region_name, latitude, longitude) VALUES (%s, %s, %s)"
        success = db_manager.postgres.execute_update(query, (data['region_name'], data['latitude'], data['longitude']))
        
        if success:
            return jsonify({'success': True, 'message': 'Region inserted successfully'}), 201
        return jsonify({'success': False, 'error': 'Failed to insert region'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/insert-biodiversity', methods=['POST'])
@role_required('Data Provider', 'Administrator')
def insert_biodiversity():
    try:
        data = request.get_json()
        # biodiversity_id, region_id, region_name, species_count, endangered_species, dominant_flora, conservation_status
        data['last_survey_date'] = datetime.utcnow()
        # Handle arrays
        if isinstance(data.get('endangered_species'), str):
            data['endangered_species'] = [s.strip() for s in data['endangered_species'].split(',') if s.strip()]
        if isinstance(data.get('dominant_flora'), str):
            data['dominant_flora'] = [s.strip() for s in data['dominant_flora'].split(',') if s.strip()]
            
        result = db_manager.mongo.insert_one('Biodiversity_Data', data)
        if result:
            return jsonify({'success': True, 'message': 'Biodiversity data inserted successfully'}), 201
        return jsonify({'success': False, 'error': 'Failed to insert biodiversity data'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/insert-air-quality', methods=['POST'])
@role_required('Data Provider', 'Administrator')
def insert_air_quality():
    try:
        data = request.get_json()
        # reading_id, region_id, aqi, co2, pm2_5, pm10, no2, so2, o3, air_quality_level
        data['recorded_at'] = datetime.utcnow()
        # Restructure pollutants if they are flat in the request
        pollutants = {
            'co2': data.pop('co2', None),
            'pm2_5': data.pop('pm2_5', None),
            'pm10': data.pop('pm10', None),
            'no2': data.pop('no2', None),
            'so2': data.pop('so2', None),
            'o3': data.pop('o3', None)
        }
        data['pollutants'] = pollutants
        
        result = db_manager.mongo.insert_one('Air_Quality_History', data)
        if result:
            return jsonify({'success': True, 'message': 'Air quality record inserted successfully'}), 201
        return jsonify({'success': False, 'error': 'Failed to insert air quality record'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/insert-species', methods=['POST'])
@role_required('Data Provider', 'Administrator')
def insert_species():
    try:
        data = request.get_json()
        # species_id, common_name, scientific_name, habitat_regions, population_estimate, conservation_status, diet, lifespan_years
        if isinstance(data.get('habitat_regions'), str):
            data['habitat_regions'] = [int(r.strip()) for r in data['habitat_regions'].split(',') if r.strip()]
            
        result = db_manager.mongo.insert_one('Species_Details', data)
        if result:
            return jsonify({'success': True, 'message': 'Species detail inserted successfully'}), 201
        return jsonify({'success': False, 'error': 'Failed to insert species detail'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/insert-sensor-metadata', methods=['POST'])
@role_required('Data Provider', 'Administrator')
def insert_sensor_metadata():
    try:
        data = request.get_json()
        # sensor_id, sensor_type, region_id, region_name, manufacturer, model, status, measurements, accuracy_rating
        data['installation_date'] = datetime.utcnow()
        if isinstance(data.get('measurements'), str):
            data['measurements'] = [m.strip() for m in data['measurements'].split(',') if m.strip()]
            
        result = db_manager.mongo.insert_one('Sensor_Metadata', data)
        if result:
            return jsonify({'success': True, 'message': 'Sensor metadata inserted successfully'}), 201
        return jsonify({'success': False, 'error': 'Failed to insert sensor metadata'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========================================
# Administrator Routes
# ========================================
@app.route('/api/users', methods=['GET'])
@role_required('Administrator')
def list_users():
    """Get all users (Admin only)"""
    try:
        users = get_all_users()
        return jsonify({
            'success': True,
            'users': users
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users', methods=['POST'])
@role_required('Administrator')
def create_user():
    """
    Create new user (Admin only).
    Expects JSON: {"name": "...", "email": "...", "password": "...", "role": "..."}
    """
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate role
        valid_roles = ['Researcher', 'Data Provider', 'Administrator']
        if data['role'] not in valid_roles:
            return jsonify({
                'success': False,
                'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'
            }), 400
        
        success = create_new_user(
            data['name'],
            data['email'],
            data['password'],
            data['role']
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'User created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create user. Email may already exist.'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Create user error: {str(e)}'
        }), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@role_required('Administrator')
def remove_user(user_id):
    """Delete user (Admin only)"""
    try:
        success = delete_user(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'User deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete user'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/query-logs', methods=['GET'])
@role_required('Administrator')
def query_logs():
    """Get query execution logs (Admin only)"""
    try:
        limit = request.args.get('limit', 50, type=int)
        logs = get_query_logs(limit)
        
        return jsonify({
            'success': True,
            'logs': logs
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/regions', methods=['GET'])
@login_required
def get_regions():
    """Get all regions (for dropdown menus)"""
    try:
        query = "SELECT region_id, region_name FROM region_info ORDER BY region_name"
        regions = db_manager.postgres.execute_query(query)
        
        return jsonify({
            'success': True,
            'regions': regions
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========================================
# Error Handlers
# ========================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ========================================
# Application Startup
# ========================================
if __name__ == '__main__':
    # Initialize database connections
    print("=" * 50)
    print("FEDERATED ENVIRONMENTAL INTELLIGENCE PLATFORM")
    print("=" * 50)
    print("\nInitializing database connections...")
    
    status = db_manager.initialize()
    
    print(f"PostgreSQL: {'✓ Connected' if status['postgres'] else '✗ Failed'}")
    print(f"MongoDB: {'✓ Connected' if status['mongo'] else '✗ Failed'}")
    print(f"Apache Drill: {'✓ Connected' if status['drill'] else '✗ Failed'}")
    
    print("\n" + "=" * 50)
    print("Starting Flask server...")
    print("Access the application at: http://localhost:5000")
    print("=" * 50 + "\n")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
