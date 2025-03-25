import mysql.connector
from mysql.connector import Error
from datetime import datetime
from dateutil.relativedelta import relativedelta
from PyQt5.QtWidgets import QMessageBox
from generarTickets.TicketIngresoMoto import generarTicketIngresoMoto
from generarTickets.TicketIngresoFijo import generarTicketIngresoFijo
from generarTickets.TicketIngresoMensualidad import generarTicketIngresoMensualidad
from generarTickets.TicketRenovarMensualidad import generarTicketRenovarMensualidad
from generarTickets.TicketReporte import generarTicketReporteCompleto
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

    def obterernuno(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()  # Devuelve una sola fila como una tupla o None si no hay resultados
        except Exception as e:
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
        query = "UPDATE registrosmoto SET fechaSalida = %s, horaSalida = %s, Total = %s WHERE id = %s"
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
    
    def editarRegistroMensualidad(self, idRegistro, nuevaPlaca,nuevoNombre,nuevoTelefono,nuevaFechaRenovacion):
        query = "UPDATE Mensualidades SET Placa = %s, Nombre = %s, Telefono= %s, fechaRenovacion=%s WHERE id = %s"
        params = (nuevaPlaca, nuevoNombre,nuevoTelefono,nuevaFechaRenovacion, idRegistro)
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
        # Verificar si el casillero con ese ID ya existe
        query_check = "SELECT Eliminado FROM Casillero WHERE id = %s"
        params_check = (Numero,)
        resultado = self.obterernuno(query_check, params_check)

        if resultado:
            # Si el casillero existe, revisar el estado de "Eliminado"
            eliminado = resultado[0]  # Extraer el valor de "Eliminado"

            if eliminado == 1:
                # Si está eliminado, actualizarlo a 0 en vez de insertar uno nuevo
                query_update = "UPDATE Casillero SET Eliminado = 0, Pc = %s, Estado = %s,Posicion=%s WHERE id = %s"
                params_update = (Pc, Estado,self.posicionDisponible(), Numero)
                self.execute_query(query_update, params_update)
            else:
                # Si ya existe y no está eliminado, mostrar mensaje
                print(f"Error: El casillero con ID {Numero} ya existe y está activo.")
        else:
            # Si no existe, insertar un nuevo registro
            query_insert = """
            INSERT INTO Casillero (id, Pc, Posicion, Estado, Eliminado)
            VALUES (%s, %s, %s, %s, 0)
            """
            params_insert = (Numero, Pc, self.posicionDisponible(), Estado)
            self.execute_query(query_insert, params_insert)


    def registrarPC(self, id, Descipcion):
        query = """
        INSERT INTO regPC (id, Descripcion)
        VALUES (%s, %s)
        """
        params = (id, Descipcion)
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
        query = "SELECT * FROM Casillero WHERE Eliminado=0;"
        return self.executeQueryReturnAll(query)
    
    def cargarTableCasilleroOrden(self):
        query = "SELECT * FROM Casillero WHERE Eliminado = 0 ORDER BY Posicion ASC;"
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

    def eliminarCasillero(self, idCasillero, posicion, estado):
        if estado == "DISPONIBLE":
            # Marcar el casillero como eliminado
            query = "UPDATE casillero SET Eliminado = 1 WHERE id = %s"
            params = (idCasillero,)
            self.execute_query(query, params)

            # Reorganizar las posiciones de los casilleros restantes
            query_update = """
            UPDATE casillero 
            SET Posicion = Posicion - 1 
            WHERE Posicion > %s AND Eliminado = 0
            """
            params_update = (posicion,)
            self.execute_query(query_update, params_update)
        else:
            print("No se puede eliminar un casillero ocupado.")

    def validarPlacaActiva(self, placa):
        query = "SELECT COUNT(*) as count FROM registrosmoto WHERE placa = %s AND fechaSalida IS NULL"
        result = self.executeQueryReturnAll(query, (placa,))
        return result[0]['count'] > 0 if result else False  # Retorna True si hay al menos un registro
    
    def validarPlacaActivaMensualidad(self, placa):
        query = "SELECT COUNT(*) as count FROM mensualidades WHERE Placa = %s"
        result = self.executeQueryReturnAll(query, (placa,))
        return result[0]['count'] > 0 if result else False  # Retorna True si hay al menos un registro
    
    def eliminarMensualidad(self, idMensualidad): 
        query = "DELETE FROM Mensualidades WHERE id = %s"
        params = (idMensualidad,)
        self.execute_query(query, params)

    def eliminarRegistroMoto (self, idRegistro,fechaSalida):
        if fechaSalida == "None":
            QMessageBox.warning(None, "Advertencia", "No puede eliminar motos que no han salido.") 
            return
        query = "DELETE FROM registrosmoto WHERE id = %s"
        params = (idRegistro,)
        self.execute_query(query, params)

    def eliminarRegistroFijo (self, idRegistro,fechaSalida):
        if fechaSalida == "None":
            QMessageBox.warning(None, "Advertencia", "No puede eliminar fijos que no han salido.") 
            return
        query = "DELETE FROM fijos WHERE id = %s"
        params = (idRegistro,)
        self.execute_query(query, params)

    def eliminarRegistroMensualidades (self, idRegistro,fechaSalida):
        if (datetime.strptime(fechaSalida, "%Y-%m-%d").date() + relativedelta(months=1)) >= datetime.now().date():
            print((datetime.strptime(fechaSalida, "%Y-%m-%d").date() + relativedelta(months=1)))
            print(datetime.now().date())
            QMessageBox.warning(None, "Advertencia", "No puede eliminar mensualidades vigentes.") 
            return
        query = "DELETE FROM mensualidades WHERE id = %s"
        params = (idRegistro,)
        self.execute_query(query, params)

    def limparRegistrosMotos(self): 
        query = "DELETE FROM registrosmoto WHERE fechaSalida != CURDATE() AND fechaSalida IS NOT NULL"
        self.execute_query(query)

    def limparRegistrosFijos(self): 
        query = "DELETE FROM fijos WHERE fechaSalida != CURDATE() AND fechaSalida IS NOT NULL"
        self.execute_query(query)

    def casillerosDisponibles(self, pc):
        query = "SELECT COUNT(*) as count FROM Casillero WHERE Estado = %s AND Pc = %s AND Eliminado = 0"
        params = ("DISPONIBLE", pc)
        result = self.executeQueryReturnAll(query, params)
        return result[0]['count'] if result else 0
    def todosCasillerosDisponibles(self):
        query = "SELECT COUNT(*) as count FROM casillero WHERE Eliminado = 0"
        result = self.executeQueryReturnAll(query)
        return result[0]['count'] if result else 0
    def contarMensualidadesActivas(self):
        query = """
        SELECT COUNT(*) as count 
        FROM Mensualidades 
        WHERE fechaUltimoPago >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        """
        result = self.executeQueryReturnAll(query,)
        return result[0]['count'] if result else 0
    def obtenerIdsRegPc(self):
        query = "SELECT id FROM regPC"
        result = self.executeQueryReturnAll(query)
        return [row['id'] for row in result] if result else []
    def casilleroAsignado(self, pc):
        query = "SELECT id FROM Casillero WHERE Pc = %s AND Estado = 'DISPONIBLE' AND Eliminado = 0 ORDER BY Posicion ASC LIMIT 1"
        params = (pc,)
        result = self.executeQueryReturnAll(query, params)
        return result[0]['id'] if result else None
    def listacasillerosDisponibles(self, pc):
        query = "SELECT id FROM Casillero WHERE Pc = %s AND Estado = 'DISPONIBLE' AND Eliminado = 0  ORDER BY Posicion ASC"
        params = (pc,)
        result = self.executeQueryReturnAll(query, params)
        return result

    def posicionDisponible(self):
        query = "SELECT COALESCE(MAX(Posicion) + 1, 1) AS siguientePosicion FROM Casillero WHERE Eliminado = 0"
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