# DatabaseConnection.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from TicketIngresoMoto import generarTicketIngresoMoto
from TicketIngresoFijo import generarTicketIngresoFijo
class DatabaseConnection:
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def open(self):
        try:
            print(f"Intentando conectar con: {self.config}")
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                port=int(self.config.get('port', 3306))
            )
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
    
    def registrarMoto(self, placa, cascos, tiempo, casillero):
        fecha_ingreso = datetime.now().strftime('%Y-%m-%d')
        hora_ingreso = datetime.now().strftime('%H:%M:%S')
        query = """
        INSERT INTO registrosMoto (Casillero, Placa, Cascos, Tipo, fechaIngreso, horaIngreso)
        VALUES (%s, %s, %s, %s, %s, %s)
        """                                                                                                      
        params = (casillero, placa, cascos, tiempo, fecha_ingreso, hora_ingreso)
        self.execute_query(query, params)
        generarTicketIngresoMoto(tiempo, placa, cascos, casillero, fecha_ingreso, hora_ingreso)
    
    def registrarFijo(self, Tipo, Nota, Valor):
            fecha_ingreso = datetime.now().strftime('%Y-%m-%d')
            hora_ingreso = datetime.now().strftime('%H:%M:%S')
            query = """
            INSERT INTO Fijos (Tipo, Nota, Valor, fechaIngreso, horaIngreso)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (Tipo, Nota, Valor, fecha_ingreso, hora_ingreso)
            self.execute_query(query, params)
            generarTicketIngresoFijo(fecha_ingreso, hora_ingreso,Tipo, Nota, Valor)
    def registrarCasillero(self, Pc, Posicion, Estado):
            query = """
            INSERT INTO Casillero (Pc, Posicion, Estado)
            VALUES (%s, %s, %s)
            """
            params = (Pc, Posicion, Estado)
            self.execute_query(query, params)
