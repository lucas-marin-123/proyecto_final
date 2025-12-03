import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error

# --- Database and GUI Configuration ---
db_config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'clasificacion_residuos', 
    'user': 'root',
    'password': 'root' 
}

# --- Configuración de Usuarios ---
AUTHORIZED_USERS = ["admin", "profe","grupo"] 
GUI_PASSWORD = "robosweeper" 

# --- Funciones de Utilidad y CRUD ---

def create_connection():
    """Crea una conexión a la base de datos."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

def fetch_data(connection, table_name):
    """Obtiene y retorna todos los registros de una tabla."""
    cursor = None
    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM `{table_name}`"
        
        cursor.execute(query)
        records = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        return column_names, records
    except Error as e:
        error_msg = f"ERROR SQL: {e.msg}"
        print(f"Error leyendo datos de '{table_name}': {error_msg}")
        # Retorna el mensaje de error como columna
        return [error_msg], [[f"No se pudieron cargar los datos."]]
    finally:
        if cursor:
            cursor.close()

def load_all_data(conn):
    """
    Función auxiliar para cargar TODAS las tablas de manera segura.
    Esta función es la que asegura que las tres tablas se consulten.
    """
    tables_to_load = ["residuos", "usuarios", "estadisticas"]
    dashboard_data = {}
    
    for table_name in tables_to_load:
        dashboard_data[table_name] = fetch_data(conn, table_name)
    
    return dashboard_data

# --- Funciones de la Interfaz (GUI) ---

def show_main_dashboard(current_username, dashboard_data): 
    """
    Crea la ventana principal de la aplicación y muestra los datos.
    """
    data_window = tk.Toplevel(root)
    data_window.title("Dashboard de Clasificación RoboSweeper")
    data_window.geometry("900x650") 
    
    data_window.protocol("WM_DELETE_WINDOW", lambda: (data_window.destroy(), root.quit())) 
    
    # 1. ENCABEZADO (igual que antes)
    header_frame = tk.Frame(data_window)
    header_frame.pack(fill='x', padx=15, pady=10)
    
    title_label = tk.Label(header_frame, 
                            text="Dashboard de Monitoreo", 
                            font=("Arial", 18, "bold"),
                            fg="#004d40") 
    title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    user_info_label = tk.Label(header_frame, 
                              text=f"Sesión activa: {current_username.upper()}", 
                              font=("Arial", 11, "italic"),
                              fg="#00796b") 
    user_info_label.grid(row=1, column=0, sticky="w")
    
    tk.Button(header_frame, 
              text="Gestionar Usuarios", 
              command=lambda: messagebox.showinfo("Info", "Funcionalidad de gestión de usuarios (To Do)"),
              font=("Arial", 10),
              bg="#e0f7fa").grid(row=0, column=1, rowspan=2, padx=(20, 0), sticky="e")
    
    header_frame.grid_columnconfigure(1, weight=1) 

    # --- ÁREA DE DATOS (TEXT AREA) ---
    # Usamos fuente Courier para alineación fija
    text_area = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=120, height=30, font=("Courier", 10))
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Definir tags para estilizar
    text_area.tag_config('header', foreground="#004d40", font=("Courier", 10, "bold"))
    text_area.tag_config('bold', font=("Courier", 10, "bold"))
    text_area.tag_config('error', foreground="red", font=("Courier", 10, "bold"))

    # Lógica de visualización de tablas
    for table_name, data_tuple in dashboard_data.items():
        columns, records = data_tuple 
        
        text_area.insert(tk.END, f"--- Registros en la tabla '{table_name.upper()}' ---\n", 'header')
        
        # 1. Verifica si hay un error SQL
        if columns and columns[0].startswith("ERROR"):
            text_area.insert(tk.END, f"🔴 {columns[0]}\n", 'error')
            
        # 2. Verifica si hay registros
        elif records and records[0] and len(records[0]) == len(columns): 
            
            # --- Formato de cabecera con alineación ---
            header_line = ""
            col_widths = [10, 25, 25, 15, 15, 15] # Anchos predefinidos para las 6 columnas posibles (máximo)
            
            # Formatear la cabecera (usando el ancho de la columna basado en el índice)
            for i, col_name in enumerate(columns):
                width = col_widths[i] if i < len(col_widths) else 15
                header_line += f"{col_name:<{width}}" # Alineación a la izquierda
            
            text_area.insert(tk.END, header_line + "\n", 'bold')
            text_area.insert(tk.END, "=" * len(header_line) + "\n")
            
            # Inserta las filas de datos
            for row in records:
                row_line = ""
                for i, cell in enumerate(row):
                    width = col_widths[i] if i < len(col_widths) else 15
                    # Asegurarse de que el dato sea tratado como string para el formateo
                    row_line += f"{str(cell):<{width}}" 
                text_area.insert(tk.END, row_line + "\n")
        
        # 3. Si no hay error, pero la tabla está vacía
        else:
            text_area.insert(tk.END, "⚠️ La tabla está vacía o el formato de datos es incorrecto.\n")
        
        text_area.insert(tk.END, "\n") # Espacio entre tablas

    # Deshabilitar edición
    text_area.config(state=tk.DISABLED)

    # === Forzar la actualización y el foco ===
    try:
        data_window.update_idletasks()
        data_window.update()       
        data_window.deiconify()         
        data_window.lift()              
    except tk.TclError as e:
        print(f"Error de Tkinter al actualizar o levantar ventana: {e}")


def login():
    """
    Verifica el login, la conexión y carga los datos en un bloque seguro.
    """
    username = username_entry.get().lower() 
    password = password_entry.get()
    
    if username in AUTHORIZED_USERS and password == GUI_PASSWORD:
        
        conn = create_connection()
        
        if conn:
            try:
                root.withdraw() 
                
                # LA FUNCIÓN load_all_data CARGA LAS TRES TABLAS
                print("Intentando cargar las 3 tablas (residuos, usuarios, estadisticas)...")
                dashboard_data = load_all_data(conn) 
                
                show_main_dashboard(username, dashboard_data)
                
            except Exception as e:
                print(f"\n--- FALLO CRÍTICO DURANTE LA CARGA O VISUALIZACIÓN ---")
                print(f"Mensaje: {e}")
                print(f"---------------------------------------------------\n")
                
                root.deiconify() 
                messagebox.showerror("Error Crítico", 
                                     f"El programa falló al cargar/mostrar datos. Consulte la consola (VS Code) para el error detallado.")
                
            finally:
                if conn.is_connected():
                    conn.close()
                    print("Conexión a la base de datos cerrada después de la carga.")
                
        else:
            messagebox.showerror("Error de Conexión", 
                                 "No se pudo conectar a la base de datos. Verifique MySQL y las credenciales.")
            root.deiconify() 
            
    else:
        messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")


# --- GUI Setup (Ventana de Login) ---
root = tk.Tk()
root.title("RoboSweeper - Login")
root.geometry("350x220") 
root.resizable(False, False)

# Título
title_login = tk.Label(root, text="Acceso al Monitoreo", font=("Arial", 14, "bold"))
title_login.pack(pady=5)

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
login_button = tk.Button(root, text="Login", command=login, bg="#004d40", fg="white")
login_button.pack(pady=10)

# Atajo de teclado: Ejecutar login al presionar Enter
root.bind('<Return>', lambda event: login())

# Iniciar la GUI
root.mainloop()