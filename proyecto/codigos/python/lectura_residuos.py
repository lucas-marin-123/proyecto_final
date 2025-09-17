import mysql.connector
from mysql.connector import Error

# Database connection details
db_config = {
    'host': 'localhost',  # Or '127.0.0.1'
    'port': 3306,        # Explicitly defining the port
    'database': 'clasificacion_residuos',
    'user': 'root',  # Replace with your MySQL username
    'password': 'root'  # Replace with your MySQL password
}

def create_connection():
    """Create a database connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connection to the database was successful!")
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

# Main script
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        # You can now use the 'conn' object to execute queries
        # (e.g., insert, select, update)
        print("Database connection is ready for use.")
        conn.close()