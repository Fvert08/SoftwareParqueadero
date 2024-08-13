import mysql.connector
from mysql.connector import Error
from datetime import datetime
from TicketIngresoMoto import generarTicketIngresoMoto
from TicketIngresoFijo import generarTicketIngresoFijo
from TicketIngresoMensualidad import generarTicketIngresoMensualidad
from TicketRenovarMensualidad import generarTicketRenovarMensualidad
from TicketReporte import generarTicketReporteCompleto
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
            self.connection.autocommit = True # se activa el auto commit
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
            # Añade 'SQL_NO_CACHE' a la consulta para evitar el uso de la caché
            query = query.replace("SELECT", "SELECT SQL_NO_CACHE", 1)
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
            # Añade 'SQL_NO_CACHE' a la consulta para evitar el uso de la caché
            query = query.replace("SELECT", "SELECT SQL_NO_CACHE", 1)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            cursor.close()

    def obtenerUltimoRegistro(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT LAST_INSERT_ID()")
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Error as e:
            print(f"Error al obtener el último registro: {e}")
            return None
        finally:
            cursor.close()  # Cerrar el cursor después de usarlo
        
    def registrarMoto(self, placa, cascos, tiempo, casillero):
        fecha_ingreso = datetime.now().strftime('%Y-%m-%d')
        hora_ingreso = datetime.now().strftime('%H:%M:%S')
        query = """
        INSERT INTO registrosMoto (Casillero, Placa, Cascos, Tipo, fechaIngreso, horaIngreso)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (casillero, placa, cascos, tiempo, fecha_ingreso, hora_ingreso)
        self.execute_query(query, params)
        # Obtener el ID del nuevo registro
        nuevo_id = self.obtenerUltimoRegistro()
        generarTicketIngresoMoto(nuevo_id,tiempo, placa, cascos, casillero, fecha_ingreso, hora_ingreso)

    def registrarMensualidad(self, placa, nombre, telefono):
        fecha_ingreso = datetime.now().strftime('%Y-%m-%d')
        hora_ingreso = datetime.now().strftime('%H:%M:%S')
        query = """
        INSERT INTO Mensualidades (Placa, Nombre, Telefono, fechaIngreso, horaIngreso,fechaUltimoPago,horaUltimoPago,fechaRenovacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (placa, nombre, telefono, fecha_ingreso, hora_ingreso, fecha_ingreso, hora_ingreso,fecha_ingreso)
        self.execute_query(query, params)
        # Obtener el ID del nuevo registro
        nuevo_id = self.obtenerUltimoRegistro()
        generarTicketIngresoMensualidad(nuevo_id,fecha_ingreso, hora_ingreso,nombre,placa,telefono)
    
    def registrarFijo(self, Tipo, Nota, Valor):
        fecha_ingreso = datetime.now().strftime('%Y-%m-%d')
        hora_ingreso = datetime.now().strftime('%H:%M:%S')
        query = """
        INSERT INTO Fijos (Tipo, Nota, Valor, fechaIngreso, horaIngreso)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (Tipo, Nota, Valor, fecha_ingreso, hora_ingreso)
        self.execute_query(query, params)

        # Obtener el ID del nuevo registro
        nuevo_id = self.obtenerUltimoRegistro()
        generarTicketIngresoFijo(nuevo_id,fecha_ingreso, hora_ingreso, Tipo, Nota, Valor)

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
        generarTicketRenovarMensualidad(str(datosBusquedarenovarMensualidad['id']),fecha_salida,hora_salida,str(datosBusquedarenovarMensualidad['Nombre']),str(datosBusquedarenovarMensualidad['Placa']),str(datosBusquedarenovarMensualidad['Telefono']), nueva_fecha)
    
    def editarRegistroMensualidad(self, idRegistro, nuevaPlaca,nuevoNombre,nuevoTelefono):
        query = "UPDATE Mensualidades SET Placa = %s, Nombre = %s, Telefono= %s WHERE id = %s"
        params = (nuevaPlaca, nuevoNombre,nuevoTelefono,idRegistro)
        self.execute_query(query, params)


    def editarRegistroFijo(self, idRegistro, nuevaTipo,nuevaNota,nuevoValor):
        query = "UPDATE Fijos SET Tipo = %s, Nota = %s, Valor= %s WHERE id = %s"
        params = (nuevaTipo, nuevaNota,nuevoValor,idRegistro)
        self.execute_query(query, params)

    def editarRegistroMoto(self, idRegistro, nuevaPlaca,nuevoCasco,nuevoTipo):
        query = "UPDATE registrosMoto SET Placa = %s, Cascos = %s, Tipo= %s WHERE id = %s"
        params = (nuevaPlaca, nuevoCasco,nuevoTipo,idRegistro)
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
    
    def cargarTableRegistrosMotosFiltrada(self,filtro,busqueda):
        if filtro == "ID":
            query = "SELECT * FROM registrosMoto WHERE id = %s;"
        elif filtro == "Casillero":
            query = "SELECT * FROM registrosMoto WHERE Casillero = %s;"
        elif filtro == "Placa":
            query = "SELECT * FROM registrosMoto WHERE Placa = %s;"
        elif filtro == "Tipo":
            query = "SELECT * FROM registrosMoto WHERE Tipo = %s;"
        params = (busqueda,)
        return self.executeQueryReturnAll(query,params)
    def cargarTableRegistrosFijosFiltrada(self,filtro,busqueda):
        if filtro == "ID":
            query = "SELECT * FROM Fijos WHERE id = %s;"
        elif filtro == "Tipo":
            query = "SELECT * FROM Fijos WHERE Tipo = %s;"
        elif filtro == "Valor":
            query = "SELECT * FROM Fijos WHERE Valor = %s;"
        params = (busqueda,)
        return self.executeQueryReturnAll(query,params)
    
    def obtenerSiguienteIDFijos(self):
        query = """
        SELECT GREATEST(
        (SELECT IFNULL(MAX(id), 0) + 1 FROM Fijos),
        (SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_NAME = 'Fijos')
        ) AS siguiente_id;
        """
        result = self.executeQueryReturnAll(query)
        return result[0]['siguiente_id'] if result else None


    def cargarTableRegistrosMensualidadFiltrada(self,filtro,busqueda):
        if filtro == "ID":
            query = "SELECT * FROM Mensualidades WHERE id = %s;"
        elif filtro == "Nombre":
            query = "SELECT * FROM Mensualidades WHERE Nombre = %s;"
        elif filtro == "Telefono":
            query = "SELECT * FROM Mensualidades WHERE Telefono = %s;"
        params = (busqueda,)
        return self.executeQueryReturnAll(query,params)
    
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
    def eliminarMensualidad(self, idMensualidad):
        query = "DELETE FROM Mensualidades WHERE id = %s"
        params = (idMensualidad,)
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
    def listacasillerosDisponibles(self, pc):
        query = "SELECT id FROM Casillero WHERE Pc = %s AND Estado = 'DISPONIBLE' ORDER BY Posicion ASC"
        params = (pc,)
        result = self.executeQueryReturnAll(query, params)
        return result

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
        
        self.execute_query(query, params)
        query = "UPDATE Casillero SET Posicion = %s WHERE Posicion = 0"
        params = (str(posicionCasillero+1),)
        self.execute_query(query, params)

    def consultarReporte (self,fechaInicio,fechaFin,Tipo):
        #--------- Definir fechas de busqueda ------------
        params = (str (fechaInicio), str(fechaFin))
        #------------ Consulta dia ---------------
        query= """
        SELECT COUNT(*) AS registrosDia, SUM(Total) AS totalDia
        FROM registrosMoto
        WHERE Tipo = 'Dia' AND fechaSalida BETWEEN %s AND %s;
        """
        resultsDia = self.executeQueryReturnAll(query,params)
        if resultsDia and resultsDia[0]['totalDia']:
            registrosDia = resultsDia[0]['registrosDia']  # El primer campo de la primera fila
            totalDia = resultsDia[0]['totalDia']      # El segundo campo de la primera fila
        else:
            registrosDia = 0
            totalDia = 0
        #------------ Consulta hora ---------------
        query = """
        SELECT COUNT(*) AS registrosHora, SUM(Total) AS totalHora
        FROM registrosMoto
        WHERE Tipo = 'Hora' AND fechaSalida BETWEEN %s AND %s;
        """
        resultsHora = self.executeQueryReturnAll(query,params)
        if resultsHora and resultsHora[0]['totalHora'] :
            registrosHora = resultsHora[0]['registrosHora']  # El primer campo de la primera fila
            totalHora = resultsHora[0]['totalHora']     # El segundo campo de la primera fila
        else:
            registrosHora = 0
            totalHora = 0
        #------------ Consulta Mensualidades ---------------
        query = """
        SELECT COUNT(*) AS registrosMes
        FROM Mensualidades
        WHERE fechaUltimoPago BETWEEN %s AND %s;
        """
        resultsMes = self.executeQueryReturnAll(query,params)
        if resultsMes:
            registrosMes = resultsMes[0]['registrosMes']  # El primer campo de la primera fila
            totalMes =   registrosMes*45000 # El segundo campo de la primera fila
        else:
            registrosMes= 0
            totalMes = 0
            
        #------------ Consulta Fijos -----------------------
        query = """
        SELECT COUNT(*) AS registrosFijos, SUM(Valor) AS totalFijos
        FROM Fijos
        WHERE fechaSalida BETWEEN %s AND %s;
        """
        resultsFijos = self.executeQueryReturnAll(query,params)
        if resultsFijos and resultsFijos[0]['totalFijos']:
            registrosFijos = resultsFijos[0]['registrosFijos']  # El primer campo de la primera fila
            totalFijos = resultsFijos[0]['totalFijos']       # El segundo campo de la primera fila
        else:
            registrosFijos = 0
            totalFijos = 0
        #--------- Generar registro del reporte --------
        fechaAcual = datetime.now().strftime('%Y-%m-%d')
        horaActual= datetime.now().strftime('%H:%M:%S')
        query = """
        INSERT INTO Reporte (Fecha, Hora, Tipo, fechaInicio, fechaFin, registrosMotosHora, totalMotosHora, registrosMotosDia, totalMotosDia,registrosMotosMes,totalMotosMes,registrosFijos,totalFijos)
        VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s)
        """
        params = (fechaAcual,horaActual,"Completo",fechaInicio,fechaFin,registrosHora,totalHora,registrosDia,totalDia,registrosMes,totalMes,registrosFijos,totalFijos)
        self.execute_query(query, params)
        nuevo_id = self.obtenerUltimoRegistro()
        generarTicketReporteCompleto(nuevo_id,Tipo,fechaAcual,horaActual,fechaInicio,fechaFin,registrosHora,totalHora,registrosDia,totalDia,registrosMes,totalMes,registrosFijos,totalFijos)
            
    def registrarSuscripcion(self):
            fechaActual = datetime.now().strftime('%Y-%m-%d')
            query = """
            INSERT INTO Suscripcion (FA)
            VALUES (%s)
            """
            params = (fechaActual,)
            self.execute_query(query, params)

    def consultarUltimaSuscripcion (self):
            query = "SELECT FA FROM Suscripcion ORDER BY FA DESC LIMIT 1"
            result = self.executeQueryReturnAll(query)
            return result[0]['FA'] if result else None