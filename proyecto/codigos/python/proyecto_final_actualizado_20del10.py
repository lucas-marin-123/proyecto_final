import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk 
import mysql.connector
from mysql.connector import Error
import datetime
import socket              
import threading           
import time                
import sys 

# --- Database and GUI Configuration ---
db_config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'clasificacion_residuos',
    'user': 'root',
    'password': 'root'
}

# --- Configuración de Usuarios ---
AUTHORIZED_USERS = ["profe", "bruno", "lucas", "paulina", "gianna", "dylan"] 
GUI_PASSWORD = "robosweeper" 

# --- Socket Configuration ---
# ¡CRÍTICO! Verifica y reemplaza con la IP local correcta de tu computadora.
TCP_IP = '172.17.0.93' 
TCP_PORT = 8888 

# --- Funciones de Utilidad y CRUD (omitiendo por brevedad) ---

def create_connection():
    """Crea una conexión a la base de datos."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

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
        print(f"Error leyendo datos de {table_name}: {e}")
        return [], []
    finally:
        cursor.close()

# --- TCP Server Logic (omitiendo por brevedad) ---
def handle_esp32_data(conn, data):
    """Analiza el dato enviado por el ESP32 e inserta en la DB."""
    try:
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
        print(f"\n[SERVIDOR TCP] ERROR: No se pudo iniciar (¿IP correcta o puerto ocupado?): {e}")
        s.close()
        return

    while root.winfo_exists(): 
        try:
            conn_socket, addr = s.accept()
            print(f"[SERVIDOR TCP] Conexión establecida desde {addr[0]}")
            
            data = conn_socket.recv(1024).decode().strip()
            
            if data:
                db_conn = create_connection()
                if db_conn:
                    handle_esp32_data(db_conn, data)
                    db_conn.close()
            
            conn_socket.close()
        except Exception as e:
            if not root.winfo_exists():
                break
            time.sleep(1) 
    s.close()
    
# --- Funciones de la Interfaz (GUI) ---

def open_user_management_window():
    """Abre una nueva ventana para gestionar usuarios."""
    user_mgmt_window = tk.Toplevel(root)
    user_mgmt_window.title("Gestión de Usuarios")
    user_mgmt_window.geometry("400x300")
    
    tk.Label(user_mgmt_window, text="Función de Gestión de Usuarios", font=("Arial", 12, "bold")).pack(pady=15)
    tk.Label(user_mgmt_window, text="Esta sección interactuaría con la tabla 'usuarios'.").pack(pady=5)


def show_main_dashboard(current_username, residuos_data, usuarios_data, estadisticas_data):
    """Crea la ventana principal de la aplicación."""
    
    data_window = tk.Toplevel(root)
    data_window.title("Dashboard de Clasificación RoboSweeper")
    data_window.geometry("800x650")
    
    # 1. ENCABEZADO (Frame con Grid)
    header_frame = tk.Frame(data_window)
    header_frame.pack(fill='x', padx=15, pady=10)
    
    # Título principal (Columna 0, Fila 0)
    title_label = tk.Label(header_frame, 
                           text="Dashboard de Monitoreo", 
                           font=("Arial", 16, "bold"),
                           fg="#004d40") 
    title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    # Etiqueta del Usuario Logueado (Columna 0, Fila 1)
    user_info_label = tk.Label(header_frame, 
                               text=f"Sesión activa: {current_username.upper()}", 
                               font=("Arial", 11, "italic"),
                               fg="#00796b") 
    user_info_label.grid(row=1, column=0, sticky="w")
    
    # Botón para Gestión de Usuarios (Columna 1, ocupa 2 filas)
    user_button = tk.Button(header_frame, 
                            text="Gestionar Usuarios", 
                            command=open_user_management_window,
                            font=("Arial", 10),
                            bg="#e0f7fa") 
    user_button.grid(row=0, column=1, rowspan=2, padx=(20, 0), sticky="e")
    
    header_frame.grid_columnconfigure(1, weight=1) 

    # --- ÁREA DE DATOS (TEXT AREA) ---
    text_area = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=100, height=30)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Lógica de visualización de tablas
    for table_name, (columns, records) in [("residuos", residuos_data), 
                                           ("usuarios", usuarios_data), 
                                           ("estadisticas", estadisticas_data)]:
        text_area.insert(tk.END, f"--- Registros en la tabla '{table_name}' ---\n")
        if records:
            header = " | ".join(columns)
            text_area.insert(tk.END, header + "\n")
            text_area.insert(tk.END, "-" * len(header) + "\n")
            for row in records:
                text_area.insert(tk.END, " | ".join(map(str, row)) + "\n")
        else:
            text_area.insert(tk.END, "No se encontraron registros.\n")
        text_area.insert(tk.END, "\n")


def login():
    """Verifica el usuario y la contraseña, inicia el servidor TCP y muestra el dashboard."""
    username = username_entry.get().lower() 
    password = password_entry.get()
    
    if username in AUTHORIZED_USERS and password == GUI_PASSWORD:
        root.withdraw() 
        
        tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
        tcp_thread.start()
        
        conn = create_connection()
        if conn:
            residuos_data = fetch_data(conn, "residuos")
            usuarios_data = fetch_data(conn, "usuarios")
            estadisticas_data = fetch_data(conn, "estadisticas")
            conn.close()
            
            show_main_dashboard(username, residuos_data, usuarios_data, estadisticas_data) 
            
    else:
        messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")


# --- GUI Setup (Ventana de Login) ---
root = tk.Tk()
root.title("RoboSweeper - Login")
root.geometry("350x300") 

# ----------------------------------------------------
# LOGO DEL PROYECTO
# ----------------------------------------------------
try:
    # 1. Nombre del archivo
    IMAGE_FILENAME = "logo.png"
    
    # 2. Cargar y redimensionar
    original_image = Image.open(IMAGE_FILENAME) 
    resized_image = original_image.resize((80, 80), Image.Resampling.LANCZOS)
    logo_img = ImageTk.PhotoImage(resized_image)
    
    # 3. Crear Label y mostrar
    logo_label = tk.Label(root, image=logo_img)
    logo_label.image = logo_img 
    logo_label.pack(pady=(15, 5)) 

except FileNotFoundError:
    print(f"Advertencia: El archivo de imagen '{IMAGE_FILENAME}' no fue encontrado. Asegúrese de que esté en la misma carpeta.")
except Exception as e:
    print(f"Error cargando la imagen (Pillow): {e}")
    
# ----------------------------------------------------

# Etiqueta y campo de USUARIO
username_label = tk.Label(root, text="Usuario:")
username_label.pack(pady=(5, 0))

username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=2)
username_entry.focus_set() 

# Etiqueta y campo de CONTRASEÑA
password_label = tk.Label(root, text="Contraseña:")
password_label.pack(pady=(5, 0)) 

password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=2)

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

# Iniciar la GUI
root.mainloop()