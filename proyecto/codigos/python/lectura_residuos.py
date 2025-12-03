import mysql.connector
from mysql.connector import Error

# --- Configuración de la Conexión ---
# ¡IMPORTANTE! Reemplaza estos valores con tus credenciales.
DB_CONFIG = {
    'host': "localhost", # O la IP de tu servidor MySQL
    'user': "root",
    'password': "root",
    'database': "clasificacion_residuos", # Nombre de tu BD
    'port': 3306
}

def leer_datos_residuos():
    """Conecta a MySQL, lee y muestra todos los datos de la tabla 'residuos'."""
    conn = None
    try:
        # 1. Establecer la conexión
        # CORRECCIÓN: Se llama a la función connect() y se le pasan los parámetros de conexión.
        conn = mysql.connector.connect(**DB_CONFIG)

        if conn.is_connected():
            cursor = conn.cursor()
            print("✅ Conexión a la base de datos MySQL exitosa.")

            # 2. Definir y Ejecutar la consulta SQL
            query = "SELECT id, tipo, fecha FROM residuos"
            cursor.execute(query)

            # 3. Obtener todos los resultados
            registros = cursor.fetchall()
            
            # 4. Imprimir los resultados
            if registros:
                print(f"\n🗑️ Se encontraron {len(registros)} registros en la tabla 'residuos':\n")
                
                # Imprimir encabezados de columna
                columnas = [i[0] for i in cursor.description]
                print(f"{columnas[0]:<5} | {columnas[1]:<10} | {columnas[2]:<20}")
                print("-" * 40)
                
                # Imprimir filas de datos
                for fila in registros:
                    # Formateo básico para alinear la salida
                    print(f"{fila[0]:<5} | {fila[1]:<10} | {fila[2]}")
            else:
                print("⚠️ La tabla 'residuos' está vacía.")
            
            # 5. Cerrar el cursor
            cursor.close()

    except Error as e:
        # Esto capturará errores como credenciales incorrectas, base de datos inexistente, etc.
        print(f"❌ Error al conectar o ejecutar la consulta: {e}")

    finally:
        # 6. Cerrar la conexión (si se llegó a abrir y está activa)
        if conn and conn.is_connected():
            conn.close()
            print("\n🔌 Conexión a MySQL cerrada.")

# --- Llamada a la función para ejecutar el código ---
if __name__ == "__main__":
    leer_datos_residuos()