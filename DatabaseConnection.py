import mysql.connector
from mysql.connector import Error
from datetime import datetime
from TicketIngresoMoto import generarTicketIngresoMoto
from TicketIngresoFijo import generarTicketIngresoFijo

class DatabaseConnection:
    _instance = None

    @staticmethod
    def get_instance(config=None):
        if DatabaseConnection._instance is None:
            if config is None:
                raise ValueError("Config must be provided for the first initialization.")
            DatabaseConnection(config)
        return DatabaseConnection._instance

    def __init__(self, config):
        if DatabaseConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseConnection._instance = self
            self.config = config
            self.connection = None

    def open(self):
        if self.connection is not None and self.connection.is_connected():
            print("La conexión a la base de datos MySQL ya está abierta.")
            return

        try:
            print("Intentando abrir la conexión a la base de datos MySQL...")
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
        self.open()
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
    
    def executeQueryReturnAll(self, query, params=None):
        self.open()
        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
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
        generarTicketIngresoFijo(fecha_ingreso, hora_ingreso, Tipo, Nota, Valor)

    def registrarSalidaMoto(self, idRegistro,totalPagado):
        fecha_salida = datetime.now().strftime('%Y-%m-%d')
        hora_salida = datetime.now().strftime('%H:%M:%S')
        query = "UPDATE registrosMoto SET fechaSalida = %s, horaSalida = %s, Total = %s WHERE id = %s"
        params = (fecha_salida, hora_salida, totalPagado, idRegistro)
        self.execute_query(query, params)
    
    def buscarMotoPorId(self, idRegistro):
        query = "SELECT * FROM registrosMoto WHERE id = %s"
        params = (idRegistro,)
        result = self.executeQueryReturnAll(query, params)
        return dict(result[0]) if result else None
    
    def buscarMotoPorPlaca(self, placaRegistro):
        query = "SELECT * FROM registrosMoto WHERE Placa = %s AND fechaSalida IS NULL"
        params = (placaRegistro,)
        result = self.executeQueryReturnAll(query, params)
        return dict(result[0]) if result else None

    def registrarCasillero(self, Numero, Pc, Estado):
        query = """
        INSERT INTO Casillero (id, Pc, Posicion, Estado)
        VALUES (%s, %s, %s,%s)
        """
        params = (Numero, Pc, self.posicionDisponible(), Estado)
        self.execute_query(query, params)

    def cargarTableRegistrosMotos(self):
        query = "SELECT * FROM registrosMoto;"
        return self.executeQueryReturnAll(query)
    
    def cargarTableCasillero(self):
        query = "SELECT * FROM Casillero;"
        return self.executeQueryReturnAll(query)
    def cargarTableCasilleroOrden(self):
        query = "SELECT * FROM Casillero ORDER BY Posicion ASC ;"
        return self.executeQueryReturnAll(query)
    
    def cargarTableRegistrosFijos(self):
        query = "SELECT * FROM Fijos;"
        return self.executeQueryReturnAll(query)
    
    def cambiarEstadoCasillero(self, idCasillero, estado):
        query = "UPDATE Casillero SET Estado = %s WHERE id = %s"
        if estado == "OCUPADO":
            params = ('DISPONIBLE', idCasillero)
        else:
            params = ('OCUPADO', idCasillero)
        self.execute_query(query, params)

    def cambiarPcCasillero(self, idCasillero, nuevoPc):
        query = "UPDATE Casillero SET Pc = %s WHERE id = %s"
        params = (nuevoPc, idCasillero)
        self.execute_query(query, params)

    def eliminarCasillero(self, idCasillero):
        query = "DELETE FROM Casillero WHERE id = %s"
        params = (idCasillero,)
        self.execute_query(query, params)

    def casillerosDisponibles(self, pc):
        query = "SELECT COUNT(*) as count FROM Casillero WHERE Estado = %s AND Pc = %s"
        params = ("DISPONIBLE", pc)
        result = self.executeQueryReturnAll(query, params)
        return result[0]['count'] if result else 0

    def casilleroAsignado(self, pc):
        query = "SELECT id FROM Casillero WHERE Pc = %s AND Estado = 'DISPONIBLE' ORDER BY Posicion ASC LIMIT 1"
        params = (pc,)
        result = self.executeQueryReturnAll(query, params)
        return result[0]['id'] if result else None
    
    def posicionDisponible(self):
        query = "SELECT COALESCE(MAX(Posicion) + 1, 1) AS siguientePosicion FROM Casillero"
        result = self.executeQueryReturnAll(query)
        return result[0]['siguientePosicion'] if result else 1
    
    def subirPosicionCasillero(self, posicionCasillero):
        if posicionCasillero <= 1:
            print("No hay posición siguiente para mover.")
            return
        query = "UPDATE Casillero SET Posicion = 0 WHERE Posicion = %s"
        params = (str(posicionCasillero),)
        self.execute_query(query, params)
        query = "UPDATE Casillero SET Posicion = %s WHERE Posicion = %s"
        params = (str (posicionCasillero), str(posicionCasillero - 1))
        self.execute_query(query, params)
        query = "UPDATE Casillero SET Posicion = %s WHERE Posicion = 0"
        params = (str(posicionCasillero-1),)
        self.execute_query(query, params)

    def bajarPosicionCasillero(self, posicionCasillero):
        if posicionCasillero >= (int(self.posicionDisponible())-1):
            print("No hay posición anterior para mover.")
            return
        query = "UPDATE Casillero SET Posicion = 0 WHERE Posicion = %s"
        params = (str(posicionCasillero),)
        self.execute_query(query, params)
        query = "UPDATE Casillero SET Posicion = %s WHERE Posicion = %s"
        params = (str (posicionCasillero), str(posicionCasillero + 1))
        self.execute_query(query, params)
        query = "UPDATE Casillero SET Posicion = %s WHERE Posicion = 0"
        params = (str(posicionCasillero+1),)
        self.execute_query(query, params)