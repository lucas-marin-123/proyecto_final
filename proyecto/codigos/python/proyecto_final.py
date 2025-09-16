import mysql.connector  # 👈 así se importa correctamente
import serial
import time

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",         # tu usuario de MySQL
    password="root",  # tu contraseña
    database="clasificacion_residuos",
)
cursor = conexion.cursor()

# Conexión al puerto serial
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

print("Esperando datos del sensor...")

while True:
    if arduino.in_waiting > 0:
        dato = arduino.readline().decode('utf-8').strip()
        print("Residuo detectado:", dato)

        sql = "INSERT INTO residuos (tipo) VALUES (%s)"
        cursor.execute(sql, (dato,))
        conexion.commit()