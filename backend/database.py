# ========================================
# Database Connection Modules
# Handles connections to PostgreSQL, MongoDB, and Apache Drill
# ========================================

import psycopg2
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient
import requests
import json
from config import POSTGRES_CONFIG, MONGODB_CONFIG, DRILL_CONFIG

# ========================================
# PostgreSQL Connection
# ========================================
class PostgresDB:
    """
    Manages PostgreSQL database connections and queries.
    Uses connection pooling for better performance.
    """
    
    def __init__(self):
        self.config = POSTGRES_CONFIG
        self.connection = None
    
    def connect(self):
        """Establish connection to PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
            return True
        except Exception as e:
            print(f"PostgreSQL Connection Error: {e}")
            return False
    
    def disconnect(self):
        """Close PostgreSQL connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=None):
        """
        Execute a SELECT query and return results as list of dictionaries.
        
        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters for safe execution
            
        Returns:
            list: Query results as list of dictionaries
        """
        try:
            if not self.connection or self.connection.closed:
                connected = self.connect()
                if not connected:
                    print("PostgreSQL Query Error: could not establish connection (check POSTGRES_PASSWORD and DB server).")
                    return None
            
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            
            # Convert to list of dictionaries
            return [dict(row) for row in results]
        except Exception as e:
            print(f"PostgreSQL Query Error: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """
        Execute INSERT, UPDATE, or DELETE query.
        
        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters for safe execution
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.connection or self.connection.closed:
                connected = self.connect()
                if not connected:
                    print("PostgreSQL Update Error: could not establish connection (check POSTGRES_PASSWORD and DB server).")
                    return False
            
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(f"PostgreSQL Update Error: {e}")
            return False
    
    def test_connection(self):
        """Test database connection"""
        try:
            result = self.execute_query("SELECT 1 as test")
            return result is not None
        except:
            return False


# ========================================
# MongoDB Connection
# ========================================
class MongoDB:
    """
    Manages MongoDB database connections and queries.
    Provides methods for CRUD operations on collections.
    """
    
    def __init__(self):
        self.config = MONGODB_CONFIG
        self.client = None
        self.db = None
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            connection_string = f"mongodb://{self.config['host']}:{self.config['port']}/"
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.config['database']]
            # Test connection
            self.client.server_info()
            return True
        except Exception as e:
            print(f"MongoDB Connection Error: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
    
    def find(self, collection_name, query={}, projection=None, limit=0):
        """
        Find documents in a collection.
        
        Args:
            collection_name (str): Name of the collection
            query (dict): MongoDB query filter
            projection (dict): Fields to include/exclude
            limit (int): Maximum number of documents to return
            
        Returns:
            list: List of documents
        """
        try:
            if self.db is None:
                self.connect()
            
            collection = self.db[collection_name]
            cursor = collection.find(query, projection)
            
            if limit > 0:
                cursor = cursor.limit(limit)
            
            results = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for doc in results:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            return results
        except Exception as e:
            print(f"MongoDB Find Error: {e}")
            return None
    
    def insert_one(self, collection_name, document):
        """
        Insert a single document into a collection.
        
        Args:
            collection_name (str): Name of the collection
            document (dict): Document to insert
            
        Returns:
            str: Inserted document ID or None
        """
        try:
            if self.db is None:
                self.connect()
            
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            print(f"MongoDB Insert Error: {e}")
            return None
    
    def update_one(self, collection_name, query, update):
        """
        Update a single document in a collection.
        
        Args:
            collection_name (str): Name of the collection
            query (dict): Filter to find the document
            update (dict): Update operations
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.db is None:
                self.connect()
            
            collection = self.db[collection_name]
            result = collection.update_one(query, {'$set': update})
            return result.modified_count > 0
        except Exception as e:
            print(f"MongoDB Update Error: {e}")
            return False
    
    def test_connection(self):
        """Test database connection"""
        try:
            if self.db is None:
                self.connect()
            self.client.server_info()
            return True
        except:
            return False


# ========================================
# Apache Drill Federated Query Engine
# ========================================
class DrillDB:
    """
    Manages Apache Drill federated queries.
    Allows querying across PostgreSQL, MongoDB, and CSV files.
    """
    
    def __init__(self):
        self.config = DRILL_CONFIG
        self.base_url = f"http://{self.config['host']}:{self.config['port']}"
    
    def execute_query(self, query):
        """
        Execute a federated SQL query through Apache Drill.
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            dict: Query results with rows and columns
        """
        try:
            # Drill REST API endpoint
            url = f"{self.base_url}/query.json"
            
            payload = {
                "queryType": "SQL",
                "query": query
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if query failed
                if data.get('queryState') == 'FAILED':
                    error_msg = data.get('errorMessage', 'Query execution failed in Drill')
                    print(f"\n{'='*60}")
                    print(f"DRILL QUERY FAILED")
                    print(f"Query: {query}")
                    print(f"Error: {error_msg}")
                    print(f"Full response: {data}")
                    print(f"{'='*60}\n")
                    return {
                        'success': False,
                        'error': error_msg,
                        'rows': [],
                        'columns': []
                    }
                
                # Query succeeded
                rows = data.get('rows', [])
                columns = data.get('columns', [])
                print(f"\n{'='*60}")
                print(f"DRILL QUERY SUCCESS")
                print(f"Query: {query[:100]}...")
                print(f"Rows returned: {len(rows)}")
                print(f"{'='*60}\n")
                
                return {
                    'success': True,
                    'rows': rows,
                    'columns': columns
                }
            else:
                return {
                    'success': False,
                    'error': f"Query failed with status {response.status_code}"
                }
        except Exception as e:
            print(f"Drill Query Error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_connection(self):
        """Test Drill connection"""
        try:
            url = f"{self.base_url}/status"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False


# ========================================
# Database Manager (Singleton Pattern)
# ========================================
class DatabaseManager:
    """
    Centralized database manager for all database connections.
    Provides a single point of access to all databases.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.postgres = PostgresDB()
            cls._instance.mongo = MongoDB()
            cls._instance.drill = DrillDB()
        return cls._instance
    
    def initialize(self):
        """Initialize all database connections"""
        postgres_ok = self.postgres.connect()
        mongo_ok = self.mongo.connect()
        drill_ok = self.drill.test_connection()
        
        return {
            'postgres': postgres_ok,
            'mongo': mongo_ok,
            'drill': drill_ok
        }
    
    def close_all(self):
        """Close all database connections"""
        self.postgres.disconnect()
        self.mongo.disconnect()


# Global database manager instance
db_manager = DatabaseManager()
