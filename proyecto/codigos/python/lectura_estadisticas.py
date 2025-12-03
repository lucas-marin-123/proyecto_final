import mysql.connector
from mysql.connector import errorcode

# --- 1. Configuración de la Conexión ---
# ¡IMPORTANTE! Reemplaza los valores con la configuración de tu MySQL Workbench/servidor.
DB_HOST = "localhost" # O la IP de tu servidor MySQL
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "clasificacion_residuos" # Reemplaza con el nombre de la base de datos donde creaste la tabla
port= 3306


# --- 2. Función para Conectar y Leer Datos ---
def leer_estadisticas():
    """Conecta a MySQL y lee los datos de la tabla 'estadisticas'."""
    cnx = None
    cursor = None
    try:
        # Intenta establecer la conexión
        cnx = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME
        )
        
        # Crea un objeto cursor para ejecutar las consultas
        cursor = cnx.cursor()

        # Consulta SQL para seleccionar todos los datos
        query = ("SELECT id, fecha, papel, plastico, organico FROM estadisticas")

        # Ejecuta la consulta
        print("Ejecutando la consulta:", query)
        cursor.execute(query)

        # Obtiene e imprime los encabezados de las columnas
        column_names = [i[0] for i in cursor.description]
        print("\n--- Columnas ---")
        print(column_names)
        print("----------------\n")
        
        # Obtiene todos los resultados y los itera
        print("--- Resultados de la Tabla estadisticas ---")
        for (id, fecha, papel, plastico, organico) in cursor:
            # Puedes acceder a los datos por nombre o por índice (como se hace aquí)
            print(f"ID: {id}, Fecha: {fecha}, Papel: {papel}, Plástico: {plastico}, Orgánico: {organico}")
        print("------------------------------------------")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: El usuario o la contraseña son incorrectos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: La base de datos no existe.")
        else:
            print(f"Ocurrió un error: {err}")
    
    finally:
        # Asegúrate de cerrar el cursor y la conexión
        if cursor:
            cursor.close()
            print("\nCursor cerrado.")
        if cnx and cnx.is_connected():
            cnx.close()
            print("Conexión a MySQL cerrada.")

# --- 3. Llamada a la Función ---
if __name__ == "__main__":
    leer_estadisticas()