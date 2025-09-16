import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpassword'),
    'database': os.getenv('DB_DATABASE', 'counter_db')
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Flag to ensure init_database runs only once
database_initialized = False

def init_database():
    """Initialize the database and create table if not exists"""
    global database_initialized
    if database_initialized:
        return

    # The database connection for initialization needs to be created without specifying a database,
    # as the database itself might not exist yet.
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS counter_db")
        cursor.execute("USE counter_db")
        
        # Create counter table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS counter (
            id INT AUTO_INCREMENT PRIMARY KEY,
            value INT NOT NULL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        
        # Insert initial counter value if table is empty
        cursor.execute("SELECT COUNT(*) FROM counter")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute("INSERT INTO counter (value) VALUES (0)")
            connection.commit()
            
        print("Database initialized successfully")
        database_initialized = True
        
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


@app.route('/api/counter', methods=['GET'])
def get_counter():
    """Get the current counter value"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT value FROM counter ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        current_value = result[0] if result else 0
        return jsonify({'value': current_value})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/api/counter/increment', methods=['POST'])
def increment_counter():
    """Increment counter value"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Get current value
        cursor.execute("SELECT value FROM counter ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        current_value = result[0] if result else 0
        
        # Increment and update
        new_value = current_value + 1
        cursor.execute("UPDATE counter SET value = %s WHERE id = (SELECT id FROM (SELECT id FROM counter ORDER BY id DESC LIMIT 1) as temp)", (new_value,))
        connection.commit()
        
        return jsonify({'value': new_value})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/counter/decrement', methods=['POST'])
def decrement_counter():
    """Decrement counter value"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Get current value
        cursor.execute("SELECT value FROM counter ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        current_value = result[0] if result else 0
        
        # Decrement and update
        new_value = current_value - 1
        cursor.execute("UPDATE counter SET value = %s WHERE id = (SELECT id FROM (SELECT id FROM counter ORDER BY id DESC LIMIT 1) as temp)", (new_value,))
        connection.commit()
        
        return jsonify({'value': new_value})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Initialize the database before running the app
init_database()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
