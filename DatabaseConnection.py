import mysql.connector
from mysql.connector import Error
from datetime import datetime
from TicketIngresoMoto import generarTicketIngresoMoto
from TicketIngresoFijo import generarTicketIngresoFijo
from TicketIngresoMensualidad import generarTicketIngresoMensualidad
from TicketRenovarMensualidad import generarTicketRenovarMensualidad
from config import DB_CONFIG
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
    def registrarMensualidad(self, placa, nombre, telefono):
        fecha_ingreso = datetime.now().strftime('%Y-%m-%d')
        hora_ingreso = datetime.now().strftime('%H:%M:%S')
        query = """
        INSERT INTO Mensualidades (Placa, Nombre, Telefono, fechaIngreso, horaIngreso,fechaUltimoPago,horaUltimoPago,fechaRenovacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (placa, nombre, telefono, fecha_ingreso, hora_ingreso, fecha_ingreso, hora_ingreso,fecha_ingreso)
        self.execute_query(query, params)
        generarTicketIngresoMensualidad(fecha_ingreso, hora_ingreso,nombre,placa,telefono)
    
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

    def registrarSalidaFijo(self, idRegistroFijo):
        fecha_salida = datetime.now().strftime('%Y-%m-%d')
        hora_salida = datetime.now().strftime('%H:%M:%S')
        query = "UPDATE Fijos SET fechaSalida = %s, horaSalida = %s WHERE id = %s"
        params = (fecha_salida, hora_salida, idRegistroFijo)
        self.execute_query(query, params)

    def registrarRenovarMensualidad(self, idRegistroMensualidad, fechaRenovacionAntigua):
        # Obtener la fecha y hora actual
        fecha_salida = datetime.now().strftime('%Y-%m-%d')
        hora_salida = datetime.now().strftime('%H:%M:%S')
        
        # Convertir la fecha antigua en un objeto datetime
        fecha_antigua = datetime.strptime(fechaRenovacionAntigua, '%Y-%m-%d')
        
        # Obtener el día de la fecha antigua
        dia_antiguo = fecha_antigua.day
        
        # Obtener el año y mes actuales
        fecha_actual = datetime.now()
        anio_actual = fecha_actual.year
        mes_actual = fecha_actual.month
        
        # Construir la nueva fecha con el año y mes actuales, manteniendo el día antiguo
        nueva_fecha = datetime(anio_actual, mes_actual, dia_antiguo).strftime('%Y-%m-%d')
        
        # Consulta SQL para actualizar las fechas
        query = """
            UPDATE Mensualidades
            SET fechaUltimoPago = %s,
                horaUltimoPago = %s,
                fechaRenovacion = %s
            WHERE id = %s
        """
        params = (fecha_salida, hora_salida, nueva_fecha, idRegistroMensualidad)
        # Ejecutar la consulta
        self.execute_query(query, params)
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        datosBusquedarenovarMensualidad= db_connection.buscarMensualidadPorId(idRegistroMensualidad)
        generarTicketRenovarMensualidad(fecha_salida,hora_salida,str(datosBusquedarenovarMensualidad['Nombre']),str(datosBusquedarenovarMensualidad['Placa']),str(datosBusquedarenovarMensualidad['Telefono']), nueva_fecha)
    
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

    def buscarMensualidadPorId(self, idRegistro):
        query = "SELECT * FROM Mensualidades WHERE id = %s"
        params = (idRegistro,)
        result = self.executeQueryReturnAll(query, params)
        return dict(result[0]) if result else None
    
    def buscarMensualidadPorPlaca(self, placaRegistro):
        query = "SELECT * FROM Mensualidades WHERE Placa = %s"
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

    def buscarFijoPorId(self, idRegistroFijo):
        query = "SELECT * FROM Fijos WHERE id = %s"
        params = (idRegistroFijo,)
        result = self.executeQueryReturnAll(query, params)
        return dict(result[0]) if result else None

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
    
    def cargarTableMensualidades(self):
        query = "SELECT * FROM Mensualidades;"
        return self.executeQueryReturnAll(query)
    
    def cargarTableUsuarios(self):
        query = "SELECT * FROM Usuarios;"
        return self.executeQueryReturnAll(query)

    def cargarTablePCAgregados(self):
        query = "SELECT * FROM regPC;"
        return self.executeQueryReturnAll(query)
    
    def cargarTableRegistros(self):
        query = "SELECT * FROM Reporte;"
        return self.executeQueryReturnAll(query)
    
    def contarTablePCAgregados(self, pc_value):
        query = "SELECT COUNT(*) AS cantidad FROM Casillero WHERE Pc = %s;"
        
        result = self.executeQueryReturnAll(query, (pc_value,))

        # Verifica el formato del resultado
        if result and len(result) > 0:
            return result[0]['cantidad']  # Devuelve el conteo usando la clave 'cantidad'
        return 0  # Retorna 0 si no hay resultados
    
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