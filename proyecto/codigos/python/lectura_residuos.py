import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error
import datetime
import socket             # Para comunicación de red (TCP)
import threading          # Para que el servidor TCP corra en segundo plano
import time               # Para la gestión de hilos

# --- Database and GUI Configuration ---
db_config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'clasificacion_residuos',
    'user': 'root',
    'password': 'root'
}

# This is the password for the GUI itself, not the database
GUI_PASSWORD = "robosweeper" 

# --- Socket Configuration ---
# ¡CRÍTICO! Reemplaza con la IP local de tu computadora.
TCP_IP = '172.17.0.93' 
TCP_PORT = 8888 

def create_connection():
    """Crea una conexión a la base de datos."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        # Usamos print() en el hilo de fondo para evitar problemas con la GUI
        print(f"Error de conexión: {e}")
        return None

# --- CRUD Functions ---

def insert_residuo(connection, tipo):
    """Inserta un nuevo registro en la tabla 'residuos'."""
    cursor = connection.cursor()
    query = "INSERT INTO residuos (tipo) VALUES (%s)"
    record = (tipo,)
    try:
        cursor.execute(query, record)
        connection.commit()
        print(f"[TCP] Dato insertado: {tipo}")
    except Error as e:
        print(f"Error insertando dato desde ESP32: '{e}'")
    finally:
        cursor.close()

def fetch_data(connection, table_name):
    """Obtiene y retorna todos los registros de una tabla."""
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        return column_names, records
    except Error as e:
        messagebox.showerror("Query Error", f"Error leyendo datos: {e}")
        return [], []
    finally:
        cursor.close()

# Las funciones display_data_window y las de insert_usuario/estadistica
# se omiten aquí por brevedad, pero se asume que están en tu código.

# --- TCP Server Logic ---

def handle_esp32_data(conn, data):
    """Analiza el dato enviado por el ESP32 e inserta en la DB."""
    try:
        # Asumiendo que el ESP32 envía una cadena simple como "Plastico"
        tipo_residuo = data.strip()
        
        if tipo_residuo:
            insert_residuo(conn, tipo_residuo)
        else:
            print("[TCP] Dato vacío recibido.")
            
    except Exception as e:
        print(f"Error al procesar el dato: {e}")

def start_tcp_server():
    """Inicia el servidor TCP en un hilo separado para escuchar al ESP32."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        print(f"\n[SERVIDOR TCP] Iniciado, escuchando en {TCP_IP}:{TCP_PORT}")
    except Exception as e:
        print(f"\n[SERVIDOR TCP] ERROR: No se pudo iniciar (¿IP correcta?): {e}")
        return

    while True:
        try:
            conn_socket, addr = s.accept()
            print(f"[SERVIDOR TCP] Conexión establecida desde {addr[0]}")
            
            # Recibir dato (máx. 1024 bytes)
            data = conn_socket.recv(1024).decode().strip()
            
            if data:
                db_conn = create_connection()
                if db_conn:
                    handle_esp32_data(db_conn, data)
                    db_conn.close()
            
            conn_socket.close()
        except Exception as e:
            # Si la ventana principal se cierra, detenemos el hilo
            if not root.winfo_exists():
                break
            time.sleep(1) 

# --- GUI Logic ---

def display_data_window(data):
    """Crea una nueva ventana para mostrar los datos obtenidos."""
    # Nota: Esta función requiere un ajuste si quieres mostrar todas las tablas
    # en una sola ventana como en tu código anterior.
    
    data_window = tk.Toplevel(root)
    data_window.title("Database Data")
    data_window.geometry("800x600")

    text_area = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=100, height=30)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Lógica para mostrar las tres tablas (residuos, usuarios, estadisticas)
    
    # ... (Se omite el código detallado de display_data_window para no repetir la respuesta anterior)

def login():
    """Verifica la contraseña, inicia el servidor TCP y muestra los datos."""
    password = password_entry.get()
    
    if password == GUI_PASSWORD:
        
        # 1. INICIA EL HILO DEL SERVIDOR TCP
        tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
        tcp_thread.start()
        
        conn = create_connection()
        if conn:
            # 2. Obtener y mostrar datos
            residuos_data = fetch_data(conn, "residuos")
            usuarios_data = fetch_data(conn, "usuarios")
            estadisticas_data = fetch_data(conn, "estadisticas")
            conn.close()
            
            # 3. Crear y popular la ventana de datos (usando la lógica de tu script original)
            data_window = tk.Toplevel(root)
            data_window.title("Database Data")
            data_window.geometry("800x600")

            text_area = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=100, height=30)
            text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            # --- Lógica de visualización de tablas ---
            for table_name, (columns, records) in [("residuos", residuos_data), ("usuarios", usuarios_data), ("estadisticas", estadisticas_data)]:
                text_area.insert(tk.END, f"--- Records in '{table_name}' table ---\n")
                if records:
                    header = " | ".join(columns)
                    text_area.insert(tk.END, header + "\n")
                    text_area.insert(tk.END, "-" * len(header) + "\n")
                    for row in records:
                        text_area.insert(tk.END, " | ".join(map(str, row)) + "\n")
                else:
                    text_area.insert(tk.END, "No records found.\n")
                text_area.insert(tk.END, "\n")
            # ----------------------------------------
            
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