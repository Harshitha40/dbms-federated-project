# ========================================
# Authentication and Authorization Module
# Handles user login, session management, and role-based access control
# ========================================

import bcrypt
from functools import wraps
from flask import session, jsonify
from database import db_manager

# ========================================
# Password Hashing Utilities
# ========================================
def hash_password(password):
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, password_hash):
    """
    Verify a password against its hash.
    
    Args:
        password (str): Plain text password to verify
        password_hash (str): Stored password hash
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except:
        return False


# ========================================
# User Authentication
# ========================================
def authenticate_user(email, password):
    """
    Authenticate a user with email and password.
    
    Args:
        email (str): User email
        password (str): User password
        
    Returns:
        dict: User information if authenticated, None otherwise
    """
    try:
        # Query user from database
        query = "SELECT user_id, name, email, password_hash, role FROM user_info WHERE email = %s"
        results = db_manager.postgres.execute_query(query, (email,))
        
        # If results is None, the DB call failed (e.g., connection issues)
        if results is None:
            print("Authentication Error: PostgreSQL unavailable")
            # Return a sentinel to indicate DB error to caller
            return {'_db_error': True}

        if not results or len(results) == 0:
            return None
        
        user = results[0]
        
        # Verify password
        if verify_password(password, user['password_hash']):
            # Return user data without password hash
            return {
                'user_id': user['user_id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        
        return None
    except Exception as e:
        print(f"Authentication Error: {e}")
        return None


def create_user_session(user_data):
    """
    Create a session for an authenticated user.
    
    Args:
        user_data (dict): User information
    """
    session['user_id'] = user_data['user_id']
    session['name'] = user_data['name']
    session['email'] = user_data['email']
    session['role'] = user_data['role']
    session['logged_in'] = True


def destroy_user_session():
    """Clear user session data"""
    session.clear()


def get_current_user():
    """
    Get current logged-in user information from session.
    
    Returns:
        dict: User information or None if not logged in
    """
    if 'logged_in' in session and session['logged_in']:
        return {
            'user_id': session.get('user_id'),
            'name': session.get('name'),
            'email': session.get('email'),
            'role': session.get('role')
        }
    return None


# ========================================
# Authorization Decorators
# ========================================
def login_required(f):
    """
    Decorator to require user to be logged in.
    Use this decorator on routes that require authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return jsonify({
                'success': False,
                'error': 'Authentication required',
                'redirect': '/login.html'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator to require specific user roles.
    Use this decorator on routes that require specific role access.
    
    Example:
        @role_required('Administrator', 'Researcher')
        def admin_route():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'logged_in' not in session or not session['logged_in']:
                return jsonify({
                    'success': False,
                    'error': 'Authentication required',
                    'redirect': '/login.html'
                }), 401
            
            user_role = session.get('role')
            if user_role not in allowed_roles:
                return jsonify({
                    'success': False,
                    'error': f'Access denied. Required role: {", ".join(allowed_roles)}',
                    'user_role': user_role
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ========================================
# User Management Functions (Admin Only)
# ========================================
def get_all_users():
    """
    Get all users from the database (without password hashes).
    Admin function only.
    
    Returns:
        list: List of user dictionaries
    """
    query = """
        SELECT user_id, name, email, role, created_at 
        FROM user_info 
        ORDER BY created_at DESC
    """
    return db_manager.postgres.execute_query(query)


def create_new_user(name, email, password, role):
    """
    Create a new user in the database.
    Admin function only.
    
    Args:
        name (str): User's full name
        email (str): User's email
        password (str): Plain text password
        role (str): User role (Researcher, Data Provider, Administrator)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if email already exists
        check_query = "SELECT email FROM user_info WHERE email = %s"
        existing = db_manager.postgres.execute_query(check_query, (email,))
        
        if existing and len(existing) > 0:
            return False  # Email already exists
        
        # Hash password
        password_hash = hash_password(password)
        
        # Insert new user
        insert_query = """
            INSERT INTO user_info (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """
        return db_manager.postgres.execute_update(
            insert_query, 
            (name, email, password_hash, role)
        )
    except Exception as e:
        print(f"Create User Error: {e}")
        return False


def delete_user(user_id):
    """
    Delete a user from the database.
    Admin function only.
    
    Args:
        user_id (int): User ID to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    query = "DELETE FROM user_info WHERE user_id = %s"
    return db_manager.postgres.execute_update(query, (user_id,))


# ========================================
# Query Logging
# ========================================
def log_query(user_id, query_text):
    """
    Log a federated query execution to the database.
    
    Args:
        user_id (int): User who executed the query
        query_text (str): The SQL query text
        
    Returns:
        bool: True if successful, False otherwise
    """
    insert_query = """
        INSERT INTO query_log (user_id, query_text)
        VALUES (%s, %s)
    """
    return db_manager.postgres.execute_update(insert_query, (user_id, query_text))


def get_query_logs(limit=50):
    """
    Get recent query logs with user information.
    Admin function only.
    
    Args:
        limit (int): Maximum number of logs to retrieve
        
    Returns:
        list: List of query log dictionaries
    """
    query = """
        SELECT 
            q.query_id,
            q.query_text,
            q.executed_at,
            u.name as user_name,
            u.email as user_email,
            u.role as user_role
        FROM query_log q
        JOIN user_info u ON q.user_id = u.user_id
        ORDER BY q.executed_at DESC
        LIMIT %s
    """
    return db_manager.postgres.execute_query(query, (limit,))
