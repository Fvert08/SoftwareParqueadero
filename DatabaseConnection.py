import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class DatabaseConnection:
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def open(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Conexión a la base de datos MySQL establecida.")
        except Error as e:
            print(f"Error al conectar con la base de datos MySQL: {e}")
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos MySQL cerrada.")
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Consulta ejecutada exitosamente.")
            return cursor
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
