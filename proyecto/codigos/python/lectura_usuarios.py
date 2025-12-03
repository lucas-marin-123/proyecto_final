import mysql.connector
from mysql.connector import errorcode

# --- 1. Configuración de la Conexión ---
# ¡IMPORTANTE! Reemplaza estos valores con tu configuración de MySQL.
DB_CONFIG = {
    'host': "localhost", 
    'user': "root",
    'password': "root",
    'database': "clasificacion_residuos", # Asegúrate de que este sea el nombre correcto de tu BD
    'port': 3306
}

def leer_usuarios():
    """Conecta a MySQL y lee todos los datos de la tabla 'usuarios'."""
    cnx = None
    cursor = None
    try:
        # Intenta establecer la conexión
        cnx = mysql.connector.connect(**DB_CONFIG)
        
        # Verifica la conexión y crea el cursor
        if cnx.is_connected():
            cursor = cnx.cursor()
            print("✅ Conexión a la base de datos MySQL exitosa.")

            # Consulta SQL para seleccionar todos los datos de la tabla 'usuarios'
            query = ("SELECT id, nombre, rol FROM usuarios")

            # Ejecuta la consulta
            print("Ejecutando la consulta:", query)
            cursor.execute(query)

            # Obtiene los encabezados de las columnas (id, nombre, rol)
            column_names = [i[0] for i in cursor.description]
            print("\n--- Columnas ---")
            print(f"{column_names[0]:<5} | {column_names[1]:<20} | {column_names[2]}")
            print("-" * 40)
            
            # Obtiene todos los resultados y los itera
            print("--- Resultados de la Tabla usuarios ---")
            
            # El bucle 'for' ahora espera (id, nombre, rol)
            for (id, nombre, rol) in cursor: 
                # Imprime cada registro formateado
                print(f"{id:<5} | {nombre:<20} | {rol}")
            
            print("--------------------------------------")
        else:
            print("⚠️ No se pudo establecer la conexión a MySQL.")

    except mysql.connector.Error as err:
        # Manejo de errores comunes
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ Error de Conexión: El usuario o la contraseña son incorrectos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("❌ Error de Base de Datos: La base de datos no existe.")
        elif err.errno == errorcode.ER_NO_SUCH_TABLE:
            print("❌ Error de Tabla: La tabla 'usuarios' no existe en la base de datos.")
        else:
            print(f"❌ Ocurrió un error inesperado: {err}")
    
    finally:
        # Asegúrate de cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()
            print("\n🔌 Conexión a MySQL cerrada.")

# --- 3. Llamada a la Función ---
if __name__ == "__main__":
    leer_usuarios()