import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error
import datetime

# Database connection details
db_config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'clasificacion_residuos',
    'user': 'root',
    'password': 'root'
}

# This is the password for the GUI itself, not the database
GUI_PASSWORD = "robosweeper" 

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Connection Error", f"Error connecting to MySQL: {e}")
        return None

def fetch_data(connection, table_name):
    """Fetch and return all records from a specified table."""
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        return column_names, records
    except Error as e:
        messagebox.showerror("Query Error", f"Error reading data: {e}")
        return [], []
    finally:
        cursor.close()

def display_data_window(data):
    """Create a new window to display the fetched data."""
    data_window = tk.Toplevel(root)
    data_window.title("Database Data")
    data_window.geometry("800x600")

    text_area = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=100, height=30)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    columns, records, table_name = data
    
    text_area.insert(tk.END, f"--- Records in '{table_name}' table ---\n")
    if records:
        header = " | ".join(columns)
        text_area.insert(tk.END, header + "\n")
        text_area.insert(tk.END, "-" * len(header) + "\n")
        for row in records:
            text_area.insert(tk.END, " | ".join(map(str, row)) + "\n")
    else:
        text_area.insert(tk.END, "No records found.\n")
    text_area.insert(tk.END, "\n\n")

def login():
    """Check the password and display data if correct."""
    password = password_entry.get()
    
    if password == GUI_PASSWORD:
        conn = create_connection()
        if conn:
            # Fetch data from all tables
            residuos_data = fetch_data(conn, "residuos")
            usuarios_data = fetch_data(conn, "usuarios")
            estadisticas_data = fetch_data(conn, "estadisticas")
            conn.close()
            
            # Create a single window to display all data
            data_window = tk.Toplevel(root)
            data_window.title("Database Data")
            data_window.geometry("800x600")

            text_area = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=100, height=30)
            text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            # Display data for residuos
            columns, records = residuos_data
            text_area.insert(tk.END, f"--- Records in 'residuos' table ---\n")
            if records:
                header = " | ".join(columns)
                text_area.insert(tk.END, header + "\n")
                text_area.insert(tk.END, "-" * len(header) + "\n")
                for row in records:
                    text_area.insert(tk.END, " | ".join(map(str, row)) + "\n")
            else:
                text_area.insert(tk.END, "No records found.\n")
            text_area.insert(tk.END, "\n")
            
            # Display data for usuarios
            columns, records = usuarios_data
            text_area.insert(tk.END, f"--- Records in 'usuarios' table ---\n")
            if records:
                header = " | ".join(columns)
                text_area.insert(tk.END, header + "\n")
                text_area.insert(tk.END, "-" * len(header) + "\n")
                for row in records:
                    text_area.insert(tk.END, " | ".join(map(str, row)) + "\n")
            else:
                text_area.insert(tk.END, "No records found.\n")
            text_area.insert(tk.END, "\n")

            # Display data for estadisticas
            columns, records = estadisticas_data
            text_area.insert(tk.END, f"--- Records in 'estadisticas' table ---\n")
            if records:
                header = " | ".join(columns)
                text_area.insert(tk.END, header + "\n")
                text_area.insert(tk.END, "-" * len(header) + "\n")
                for row in records:
                    text_area.insert(tk.END, " | ".join(map(str, row)) + "\n")
            else:
                text_area.insert(tk.END, "No records found.\n")
            text_area.insert(tk.END, "\n")
            
    else:
        messagebox.showerror("Error", "Incorrect password")

# --- GUI Setup ---
root = tk.Tk()
root.title("Login to Database")
root.geometry("300x150")

# Label for the password field
password_label = tk.Label(root, text="Enter Password:")
password_label.pack(pady=5)

# Entry widget for the password
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

# Start the GUI
root.mainloop()