import subprocess
import mysql.connector

# Instalar las librerías necesarias
subprocess.run(["pip", "install", "PyQt5"])
subprocess.run(["pip", "install", "mysql-connector-python"])

# Conectar a MySQL y crear la base de datos y las tablas
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="tu_usuario",
        password="tu_contraseña"
    )

    cursor = connection.cursor()

    # Crear base de datos
    cursor.execute("CREATE DATABASE IF NOT EXISTS nombre_base_de_datos")

    # Seleccionar la base de datos recién creada
    cursor.execute("USE nombre_base_de_datos")

    # Crear tablas y columnas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabla_ejemplo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            columna1 VARCHAR(255),
            columna2 INT
        )
    """)

    # Agregar más tablas y columnas si es necesario

    connection.commit()
    print("Base de datos y tablas creadas exitosamente.")

except mysql.connector.Error as error:
    print("Error al conectar a MySQL:", error)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()