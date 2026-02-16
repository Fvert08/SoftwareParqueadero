from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import Qt,QSize
from DatabaseConnection import DatabaseConnection
from config import DB_CONFIG
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from datetime import datetime
from generarTickets.TicketSalidaMotos import generarTicketSalidaMoto
from generarTickets.TicketSalidaFijo import generarTicketSalidaFijo
from generarTickets.TicketRenovarMensualidad import generarTicketRenovarMensualidad
from leerTxt import leer_archivo,leer_archivoDesencriptado
from ui_styles import BUTTON_STYLE_DARK_25_10_20, BUTTON_STYLE_TICKETS_DISABLED, BUTTON_STYLE_TICKETS_PRIMARY, LABEL_STYLE_30_WHITE, LABEL_STYLE_40_WHITE, LINE_STYLE_WHITE, TEXTBOX_STYLE_30, TEXTBOX_STYLE_40, TITLE_STYLE_30_GRAY_BOLD, TITLE_STYLE_30_WHITE_BOLD
class PaginaTickets(QWidget):
    senalActualizarTablasCasilleros= pyqtSignal()
    senalActualizarTablaRegistroMotos = pyqtSignal()
    senalActualizarTablaRegistroFijos = pyqtSignal()
    senalActualizarTablaRegistroMensualidades = pyqtSignal()
    senalActualizarTexboxCodigoFijos = pyqtSignal()
    senalActualizarTextboxMensualidadesVigentes = pyqtSignal()
    senalActualizarResumen = pyqtSignal()
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()
        self.casilleros_disponibles = []
        self.indice_actual = 0

    def calcularTiempoTranscurrido (self,horaIngreso,fechaIngreso,fechaHoraARestar):
          # Convertir timedelta a un objeto time
        horaIngreso_time = (datetime.min + horaIngreso).time()
        # Combinar fecha y hora de ingreso en un objeto datetime
        fechaHoraIngreso = datetime.combine(fechaIngreso, horaIngreso_time)
        # Calcular la diferencia
        diferencia = fechaHoraARestar - fechaHoraIngreso
            # Obtener horas, minutos y segundos
        horas, resto = divmod(diferencia.total_seconds(), 3600)
        minutos, segundos = divmod(resto, 60)
        # Formatear el resultado
        return  horas,minutos,segundos

    def _set_boton_interactivo(self, boton, enabled):
        boton.setEnabled(enabled)
        boton.setAttribute(Qt.WA_TransparentForMouseEvents, not enabled)

    def _actualizarEstadoBotonMotoIngreso(self):
        self._set_boton_interactivo(self.botonImprimirRegistroMoto, bool(self.textboxPlacaIngresoMoto.text().strip()))

    def _actualizarEstadoBotonMotoSalida(self):
        self._set_boton_interactivo(self.boton_facturar, bool(self.textboxFIngresoSacarMoto.text().strip()))

    def _actualizarEstadoBotonFijoIngreso(self):
        self._set_boton_interactivo(
            self.botonImprimirFijo,
            bool(self.textboxNotaFijoIngreso.text().strip()) and bool(self.textboxValorFijo.text().strip())
        )

    def _actualizarEstadoBotonFijoSalida(self):
        self._set_boton_interactivo(self.botonfacturarFijos, bool(self.textboxFIngresoFijos.text().strip()))

    def _actualizarEstadoBotonMensualidadIngreso(self):
        self._set_boton_interactivo(
            self.botonImprimirMensualidad,
            bool(self.textboxPlacaMensualidad.text().strip())
            and bool(self.textboxNombreMensualidad.text().strip())
            and bool(self.textboxTelefonoMensualidad.text().strip())
        )

    def _actualizarEstadoBotonRenovarMensualidad(self):
        self._set_boton_interactivo(self.botonRenovarMensualidad, bool(self.textboxFechaIngresoRenovarMensualidad.text().strip()))

    def cargarBusquedaSalidaFijo (self):
        datosBusquedaSalidaFijos = None
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        if self.textboxCodigoFijo.text():
            datosBusquedaSalidaFijos= db_connection.buscarFijoPorId(self.textboxCodigoFijo.text())      
        if datosBusquedaSalidaFijos:
            self.textboxTipoFijos.setText(str(datosBusquedaSalidaFijos['Tipo']))
            self.textboxNotaFijos.setText(str(datosBusquedaSalidaFijos['Nota']))
            self.textboxFIngresoFijos.setText(str(datosBusquedaSalidaFijos['fechaIngreso']))
            self.textboxHIngresoFijos.setText(str(datosBusquedaSalidaFijos['horaIngreso']))
            self.textboxTotalApagarFijos.setText(str(datosBusquedaSalidaFijos['Valor']))
            if datosBusquedaSalidaFijos['fechaSalida']: #Si ya fue registrada mostrarlos datos
                self.textboxHSalidaFijos.setText(str(datosBusquedaSalidaFijos['horaSalida']))
                self.textboxFSalidaFijos.setText(str(datosBusquedaSalidaFijos['fechaSalida']))
                # Convertir timedelta a un objeto time
                horaSalida_time = (datetime.min + datosBusquedaSalidaFijos['horaSalida']).time()
                # Combinar fecha y hora de ingreso en un objeto datetime
                fechaHoraSalida = datetime.combine(datosBusquedaSalidaFijos['fechaSalida'], horaSalida_time)
                horas,minutos,segundos = self.calcularTiempoTranscurrido(datosBusquedaSalidaFijos['horaIngreso'], datosBusquedaSalidaFijos['fechaIngreso'],fechaHoraSalida)
                resultado = f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"
                self.textboxTiempoTotalFijos.setText(resultado)
                self._set_boton_interactivo(self.botonfacturarFijos, False)#Deshabilitar botón para imprimir
            else:#Si no, calcular el tiepo y el total a pagar
                fechaActual = datetime.now().strftime('%Y-%m-%d')
                horaActual = datetime.now().strftime('%H:%M:%S')
                self.textboxFSalidaFijos.setText(str(fechaActual))
                self.textboxHSalidaFijos.setText(str(horaActual))
                #Calcular tiempo transcurrido
                horas,minutos,segundos = self.calcularTiempoTranscurrido(datosBusquedaSalidaFijos['horaIngreso'], datosBusquedaSalidaFijos['fechaIngreso'],datetime.now())
                resultado = f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"
                self.textboxTiempoTotalFijos.setText(resultado)
                self._actualizarEstadoBotonFijoSalida()
        else:
            print("No se encontraron registros")

    def cargarBusquedaRenovarMensualidad (self):
        datosBusquedaRenovarMensualidad = None
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        if self.textboxCodigoRenovarMensualidad.text():
            datosBusquedaRenovarMensualidad= db_connection.buscarMensualidadPorId(self.textboxCodigoRenovarMensualidad.text())
        else:
            if self.textboxPlacaRenovarMensualidad.text():
                datosBusquedaRenovarMensualidad= db_connection.buscarMensualidadPorPlaca(self.textboxPlacaRenovarMensualidad.text())    
        if datosBusquedaRenovarMensualidad:
            self.textboxCodigoRenovarMensualidad.setText(str(datosBusquedaRenovarMensualidad['id']))
            self.textboxPlacaRenovarMensualidad.setText(str(datosBusquedaRenovarMensualidad['Placa']))
            self.textboxNombreRenovarMensualidad.setText(str(datosBusquedaRenovarMensualidad['Nombre']))
            self.textboxTelefonoRenovarMensualidad.setText(str(datosBusquedaRenovarMensualidad['Telefono']))
            self.textboxFechaIngresoRenovarMensualidad.setText(str(datosBusquedaRenovarMensualidad['fechaIngreso']))
            self.textboxFechaUPagoRenovarMensualidad.setText(str(datosBusquedaRenovarMensualidad['fechaUltimoPago']))
            self.textboxFechaRenovacionRenovarMensualidad.setText(str(datosBusquedaRenovarMensualidad['fechaRenovacion']))
            self.textboxHoraIngresoRenovarMensualidad.setText(str(datosBusquedaRenovarMensualidad['horaIngreso']))
            self.textboxHoraUPagoRenovarMensualidad.setText(str(datosBusquedaRenovarMensualidad['horaUltimoPago']))
            self.textboxTotalAPagarRenovarMensualidad.setText(str("$45.000"))
            self._actualizarEstadoBotonRenovarMensualidad()
        else:
            print("No se encontraron registros")
            
    def cargarBusquedaSalidaMoto (self):
        datosBusquedaSalidaMoto = None
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        if self.textboxCodigoSacarMoto.text():
            datosBusquedaSalidaMoto= db_connection.buscarMotoPorId(self.textboxCodigoSacarMoto.text())
        else:
            if self.textboxPlacaSacarMoto.text():
                datosBusquedaSalidaMoto= db_connection.buscarMotoPorPlaca(self.textboxPlacaSacarMoto.text()) 
                print (f"placa a buscar: {self.textboxPlacaSacarMoto.text()}")
        if datosBusquedaSalidaMoto:
            self.textboxCodigoSacarMoto.setText(str(datosBusquedaSalidaMoto['id']))
            self.textboxPlacaSacarMoto.setText(str(datosBusquedaSalidaMoto['Placa']))
            self.textboxCasilleroSacarMoto.setText(str(datosBusquedaSalidaMoto['Casillero']))
            self.textboxCascosSacarMoto.setText(str(datosBusquedaSalidaMoto['Cascos']))
            self.textboxPagadoPorSacarMoto.setText(str(datosBusquedaSalidaMoto['Tipo']))
            self.textboxFIngresoSacarMoto.setText(str(datosBusquedaSalidaMoto['fechaIngreso']))
            self.textboxHIngresoSacarMoto.setText(str(datosBusquedaSalidaMoto['horaIngreso']))
            if datosBusquedaSalidaMoto['fechaSalida']: #Si ya fue registrada mostrarlos datos
                self.textboxFSalidaSacarMoto.setText(str(datosBusquedaSalidaMoto['fechaSalida']))
                self.textboxHSalidaSacarMoto.setText(str(datosBusquedaSalidaMoto['horaSalida']))
                self.textboxTotalAPagarSacarMoto.setText(str(datosBusquedaSalidaMoto['Total']))
                # Convertir timedelta a un objeto time
                horaSalida_time = (datetime.min + datosBusquedaSalidaMoto['horaSalida']).time()
                # Combinar fecha y hora de ingreso en un objeto datetime
                fechaHoraSalida = datetime.combine(datosBusquedaSalidaMoto['fechaSalida'], horaSalida_time)
                horas,minutos,segundos = self.calcularTiempoTranscurrido(datosBusquedaSalidaMoto['horaIngreso'], datosBusquedaSalidaMoto['fechaIngreso'],fechaHoraSalida)
                resultado = f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"
                self.textboxTiempoTotalSacarMoto.setText(resultado)
                self._set_boton_interactivo(self.boton_facturar, False)#Deshabilitar botón para imprimir

            else:#Si no, calcular el tiepo y el total a pagar
                fechaActual = datetime.now().strftime('%Y-%m-%d')
                horaActual = datetime.now().strftime('%H:%M:%S')
                self.textboxFSalidaSacarMoto.setText(str(fechaActual))
                self.textboxHSalidaSacarMoto.setText(str(horaActual))
                #Calcular tiempo transcurrido
                horas,minutos,segundos = self.calcularTiempoTranscurrido(datosBusquedaSalidaMoto['horaIngreso'], datosBusquedaSalidaMoto['fechaIngreso'],datetime.now())
                resultado = f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"
                self.textboxTiempoTotalSacarMoto.setText(resultado)
                # Cambiar estas variables segun los precios a cobrar del parqueadero
                cobroPorHora= int(leer_archivoDesencriptado('config','VH.txt')) #Cobro por hora del parqueadero
                cobroPorDia = int(leer_archivoDesencriptado('config','VD.txt')) #Cobro ppr dia del parqueadero
                #-------------------------------------------------------------------
                if (minutos or segundos)>0: #Si Se lleva a subre pasar un segundo o un minuto de más se cobrará una hora completa
                    horas+=1
                if str(datosBusquedaSalidaMoto['Tipo']) == "Dia":
                    self.totalAPagarSacarMoto = cobroPorDia
                else:
                    self.totalAPagarSacarMoto = horas*cobroPorHora
                self.textboxTotalAPagarSacarMoto.setText(f"${str(self.totalAPagarSacarMoto)}")
                self._actualizarEstadoBotonMotoSalida()
        else:
            print("No se encontraron registros")

    def actualizarTextboxCasilleros(self):
        """Actualiza los textbox de casilleros disponibles"""
        self.casilleros_disponibles = []
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        
        # Si no hay cascos, asignar directamente casillero 0
        if self.combobox_cascos.currentText() == "0":
            self.textbox_casillero.setText("0")
        else:
            # Asignar casillero disponible en caso de no haber casillero se asigna el 0
            casillero = db_connection.casilleroAsignado(leer_archivo('config','PcActual.txt'))
            self.textbox_casillero.setText(str(casillero) if casillero else "0")
        
        # Actualizar contador de disponibles
        self.textbox_casillerosDis.setText(
            str(db_connection.casillerosDisponibles(leer_archivo('config','PcActual.txt')))
        )
        self._actualizarEstadoBotonMotoIngreso()
    
    def actualizarMensualidadesVigentes (self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        self.textbox_MensualidadesVigentes.setText(str(db_connection.contarMensualidadesActivas()))
    def initUI(self):
        #----Paginas
        #Pagina del menú
        page_registrosMenu = QWidget()
        #Pagina principal
        page_principalTickets = QWidget()

        # -----Stack para agregar todas las pantallas de tickets
        self.stacked_widgetTickets = QStackedWidget()
        
        #--------#layouts (Izquierdo, derecho y principal)
        #layout Menu derecho donde se agregan todos los botones
        layout_ticketsmenu = QGridLayout()
        
        #layout principal box horizontal
        main_layoutRegistros = QHBoxLayout()
        #Se llaman las pantallas para cargarlas en el stack
        self.pantallaIngresoMotos()
        self.pantallaSacarMoto()
        self.pantallaIngresarFijo()
        self.pantallaSacarFijo()
        self.pantallaIngresarMensualidad()
        self.pantallaRenovarMensualidad()
        #------------------------Menu lateral---------------------------
        # Crear la línea vertical de 1 pixel y añadirla a la cuadrícula
        linea_vertical = QFrame()
        linea_vertical.setFrameShape(QFrame.VLine)
        linea_vertical.setLineWidth(1)
        linea_vertical.setStyleSheet(LINE_STYLE_WHITE)
        layout_ticketsmenu.addWidget(linea_vertical, 0, 0, 8, 1)
        # Crear la sección derecha con el título "Menú"
        titulo_menu = QLabel('Menú')
        titulo_menu.setStyleSheet(TITLE_STYLE_30_GRAY_BOLD)
        layout_ticketsmenu.addWidget(titulo_menu, 0, 1, 1, 2, Qt.AlignCenter)
        linea_horizontal2 = QFrame()
        linea_horizontal2.setFrameShape(QFrame.HLine)
        linea_horizontal2.setLineWidth(1)
        linea_horizontal2.setStyleSheet(LINE_STYLE_WHITE)
        layout_ticketsmenu.addWidget(linea_horizontal2, 1, 1, 1, 2)

        # Crea un boton para ingresar a generar ticket ingresar moto
        boton_IngresarM = QPushButton()
        boton_IngresarM.setStyleSheet(self._menu_lateral_style())
        boton_IngresarM.setIcon(QIcon('imagenes/IngresoMoto.png'))  # Establecer el icono
        boton_IngresarM.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarM, 2, 1, 1, 1)
        boton_IngresarM.setCheckable(True)
        boton_IngresarM.setChecked(True)
        boton_IngresarM.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(0))


        # Crea un boton para ingresar a generar ticket sacar moto
        boton_SacarM = QPushButton()
        boton_SacarM.setStyleSheet(self._menu_lateral_style())
        boton_SacarM.setIcon(QIcon('imagenes/SalidaMoto.png'))  # Establecer el icono
        boton_SacarM.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarM, 2, 2, 1, 1)
        boton_SacarM.setCheckable(True)
        boton_SacarM.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(1))


        # Crea un boton para ingresar a generar ticket ingresar Fijo
        boton_IngresarF = QPushButton()
        boton_IngresarF.setStyleSheet(self._menu_lateral_style())
        boton_IngresarF.setIcon(QIcon('imagenes/IngresoFijo.png'))  # Establecer el icono
        boton_IngresarF.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarF, 3, 1, 1, 1)
        boton_IngresarF.setCheckable(True)
        boton_IngresarF.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(2))

        # Crea un boton para ingresar a generar ticket sacar Fijo
        boton_SacarF = QPushButton()
        boton_SacarF.setStyleSheet(self._menu_lateral_style())
        boton_SacarF.setIcon(QIcon('imagenes/SalidaFijo.png'))  # Establecer el icono
        boton_SacarF.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarF, 3, 2, 1, 1)
        boton_SacarF.setCheckable(True)
        boton_SacarF.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(3))
        
        #Crea un boton para ingresar a generar ticket ingresar Mensualidad
        boton_IngresarMensualidad = QPushButton()
        boton_IngresarMensualidad.setStyleSheet(self._menu_lateral_style())
        boton_IngresarMensualidad.setIcon(QIcon('imagenes/Mesingreso.png'))  # Establecer el icono
        boton_IngresarMensualidad.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarMensualidad, 4, 1, 1, 1)
        boton_IngresarMensualidad.setCheckable(True)
        boton_IngresarMensualidad.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(4))

        #Crea un boton para ingresar a generar ticket sacar Mensualidad
        boton_SacarMensualidad = QPushButton()
        boton_SacarMensualidad.setStyleSheet(self._menu_lateral_style())
        boton_SacarMensualidad.setIcon(QIcon('imagenes/Mesrenovar.png'))  # Establecer el icono
        boton_SacarMensualidad.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarMensualidad,   4, 2, 1, 1)
        boton_SacarMensualidad.setCheckable(True)
        boton_SacarMensualidad.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(5))

        for boton_menu in [boton_IngresarM, boton_SacarM, boton_IngresarF, boton_SacarF, boton_IngresarMensualidad, boton_SacarMensualidad]:
            boton_menu.setAutoExclusive(True)

        #Se agrega el layout del menú a la página del menú
        page_registrosMenu.setLayout(layout_ticketsmenu)
        #Se agrega el stack al layout principal
        main_layoutRegistros.addWidget(self.stacked_widgetTickets)
        #se agrega el menú al layout principal
        main_layoutRegistros.addWidget(page_registrosMenu)
        #se agrega el layout principal a la pagina principal
        page_principalTickets.setLayout(main_layoutRegistros)
        #se llama la primera posición del stack
        self.stacked_widgetTickets.setCurrentIndex(0)
        #se agrega toda la pagina al stack principal de la app
        self.stacked_widget.addWidget(page_principalTickets)

    def _menu_lateral_style(self):
        return (
            "QPushButton{color:#737074;background-color:#151419;font-size:30px;border:none;"
            "border-radius:15px;padding:10px 10px;}"
            "QPushButton:hover{background-color:#1f1e24;color:#ffffff;}"
            "QPushButton:checked{background-color:#222125;color:#ffffff;}"
            "QPushButton:checked:hover{background-color:#222125;color:#ffffff;}"
        )
    def siguienteCasilleroDisponible(self, pc):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        if not self.casilleros_disponibles:       
            self.casilleros_disponibles = db_connection.listacasillerosDisponibles(pc)
        if not self.casilleros_disponibles:
            self.casilleros_disponibles = []
            return 0
        # Obtener el casillero actual y avanzar al siguiente
        casillero_actual = self.casilleros_disponibles[self.indice_actual]['id']
        self.indice_actual = (self.indice_actual + 1) % len(self.casilleros_disponibles)
        return casillero_actual
    
    def pantallaIngresoMotos (self):
         # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Pagina de ticketes ingreso
        page_tickets = QWidget()
        #layout de el registro de los tickets
        layout_ticketsIngresoMotos = QGridLayout()
        #------------------------Ingreso de motos------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_tickets = QLabel('REGISTRAR INGRESO MOTO')
        titulo_tickets.setStyleSheet("color: #888888;font-size: 25px; font-weight: bold;")
        layout_ticketsIngresoMotos.addWidget(titulo_tickets, 0, 0, 1, 4, Qt.AlignCenter|Qt.AlignTop)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINE_STYLE_WHITE)
        layout_ticketsIngresoMotos.addWidget(linea_horizontal1, 1, 0, 1, 4)

        # Crear el label "Placa" y la textbox
        label_placa = QLabel('Placa:')
        label_placa.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsIngresoMotos.addWidget(label_placa, 3, 1, 1, 1,Qt.AlignRight)

        self.textboxPlacaIngresoMoto = QLineEdit()
        self.textboxPlacaIngresoMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsIngresoMotos.addWidget(self.textboxPlacaIngresoMoto, 3, 2, 1, 1,Qt.AlignLeft)
        self.textboxPlacaIngresoMoto.textChanged.connect(lambda: self.textboxPlacaIngresoMoto.setText(self.textboxPlacaIngresoMoto.text().upper()))
        self.textboxPlacaIngresoMoto.textChanged.connect(self._actualizarEstadoBotonMotoIngreso)

        # Crear el label "Cascos" y el combobox
        label_cascos = QLabel('Cascos:')
        label_cascos.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsIngresoMotos.addWidget(label_cascos, 5, 1, 1, 1,Qt.AlignRight)

        self.combobox_cascos = QComboBox()
        self.combobox_cascos.addItems(['0', '1', '2'])
        self.combobox_cascos.setStyleSheet(TEXTBOX_STYLE_40)
        layout_ticketsIngresoMotos.addWidget(self.combobox_cascos, 5, 2, 1, 1,Qt.AlignLeft)
        self.combobox_cascos.currentTextChanged.connect(
            lambda: self.textbox_casillero.setText("0") 
            if self.combobox_cascos.currentText() == "0" 
            else self.textbox_casillero.setText(str(db_connection.casilleroAsignado(leer_archivo('config','PcActual.txt'))))
)


        # Crear el label "Tiempo" y el combobox
        label_Tiempo = QLabel('Tiempo:')
        label_Tiempo.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsIngresoMotos.addWidget(label_Tiempo, 7, 1, 1, 1,Qt.AlignRight)

        combobox_Tiempo = QComboBox()
        combobox_Tiempo.addItems(['Hora', 'Dia'])
        combobox_Tiempo.setStyleSheet(TEXTBOX_STYLE_40)
        layout_ticketsIngresoMotos.addWidget(combobox_Tiempo, 7, 2, 1, 1,Qt.AlignLeft)

        # Crea una checkbox para confirmar que se eligio dia o mes  en "combobox_Tiempo"
        checkbox_opcion = QCheckBox('Confirmar', page_tickets)
        checkbox_opcion.setStyleSheet("color: #FFFFFF; font-size: 20px;")
        checkbox_opcion.setChecked(False)  # Opcional: Puedes establecer si la casilla está marcada por defecto o no
        layout_ticketsIngresoMotos.addWidget(checkbox_opcion, 7, 3, 1, 1,Qt.AlignLeft)
        # Crear el label "Casillero" y el combobox
        label_casillero = QLabel('Casillero:', page_tickets)
        label_casillero.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsIngresoMotos.addWidget(label_casillero, 9, 1, 1, 1,Qt.AlignRight)  # Alineamiento arriba y a la izquierda
        self.textbox_casillero = QLineEdit(page_tickets)
        self.textbox_casillero.setStyleSheet(TEXTBOX_STYLE_30)
        self.textbox_casillero.setFixedWidth(60)
        self.textbox_casillero.setReadOnly(True)
        layout_ticketsIngresoMotos.addWidget(self.textbox_casillero, 9, 2, 1, 1,Qt.AlignLeft)  # Alineamiento arriba y a la izquierda
        self.textbox_casillero.setText(str(db_connection.casilleroAsignado(leer_archivo('config','PcActual.txt'))))

        # Crea un boton para cambiar al siguiente casillero disponible
        boton_cambiarcasillero = QPushButton('Siguiente', page_tickets)
        boton_cambiarcasillero.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 15px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #666666;
            }
        """)
        layout_ticketsIngresoMotos.addWidget(boton_cambiarcasillero, 9, 3, 1, 1)

        # CORRECCIÓN: Solo permitir cambiar si hay cascos
        boton_cambiarcasillero.clicked.connect(lambda: [
            self.textbox_casillero.setText(
                str(self.siguienteCasilleroDisponible(leer_archivo('config','PcActual.txt')))
            ) if self.combobox_cascos.currentText() != "0" else None
        ])
        # Crear el label "Casilleros disponibles" y el combobox
        label_casillerosDis = QLabel('Casilleros disponibles:', page_tickets)
        label_casillerosDis.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsIngresoMotos.addWidget(label_casillerosDis, 11, 1, 1, 1,Qt.AlignRight)  # Alineamiento arriba y a la izquierda
        #Crear Textbox "Casilleros disponibles" 
        self.textbox_casillerosDis = QLineEdit(page_tickets)
        self.textbox_casillerosDis.setStyleSheet(TEXTBOX_STYLE_30)
        self.textbox_casillerosDis.setReadOnly(True)
        self.textbox_casillerosDis.setFixedWidth(60)
        self.textbox_casillerosDis.setText(str(db_connection.casillerosDisponibles(leer_archivo('config','PcActual.txt'))))
        layout_ticketsIngresoMotos.addWidget(self.textbox_casillerosDis, 11, 2, 1, 1,Qt.AlignLeft)  # Alineamiento arriba y a la izquierda
        # Crea un boton para Imprimir
        self.botonImprimirRegistroMoto = QPushButton('Imprimir', page_tickets)
        self.botonImprimirRegistroMoto.setStyleSheet(BUTTON_STYLE_TICKETS_DISABLED)
        self._set_boton_interactivo(self.botonImprimirRegistroMoto, False)
        layout_ticketsIngresoMotos.addWidget(self.botonImprimirRegistroMoto, 13, 2, 1, 1)
        # Conectar el botón de imprimir a la función registrarMoto
        self.botonImprimirRegistroMoto.clicked.connect(lambda: [
            # Validaciones
            QMessageBox.warning(None, "Advertencia", "Debe ingresar una placa.") 
            if not self.textboxPlacaIngresoMoto.text().strip() else 
            QMessageBox.warning(None, "Advertencia", "Esta placa aun tiene un registro activo.") 
            if db_connection.validarPlacaActiva(self.textboxPlacaIngresoMoto.text()) else 
            QMessageBox.warning(None, "Advertencia", "Debe seleccionar la opción en la casilla si el tiempo es 'Día'.") 
            if combobox_Tiempo.currentText() == "Dia" and not checkbox_opcion.isChecked() else [

                # Registrar moto (ahora cambia el estado del casillero internamente)
                db_connection.registrarMoto(
                    self.textboxPlacaIngresoMoto.text(),
                    self.combobox_cascos.currentText(),
                    combobox_Tiempo.currentText(),
                    self.textbox_casillero.text(),
                ),

                # Limpiar campos
                self.textboxPlacaIngresoMoto.clear(),
                self.combobox_cascos.setCurrentIndex(0),
                combobox_Tiempo.setCurrentIndex(0),
                checkbox_opcion.setChecked(False),

                # YA NO ES NECESARIO cambiar el estado aquí
                # (registrarMoto() ya lo hace automáticamente)

                # Actualizar UI
                self.actualizarTextboxCasilleros(),
                self.senalActualizarTablasCasilleros.emit(),
                self.senalActualizarTablaRegistroMotos.emit(),
            ]
        ])

        layout_ticketsIngresoMotos.setRowStretch(1, 1)
        layout_ticketsIngresoMotos.setRowStretch(2, 1)
        layout_ticketsIngresoMotos.setRowStretch(4, 1)
        layout_ticketsIngresoMotos.setRowStretch(6, 1)
        layout_ticketsIngresoMotos.setRowStretch(8, 1)
        layout_ticketsIngresoMotos.setRowStretch(10, 1)
        layout_ticketsIngresoMotos.setRowStretch(12, 1)
       

        page_tickets.setLayout(layout_ticketsIngresoMotos)
        #se agrega la pagina al stack
        self.stacked_widgetTickets.addWidget(page_tickets)
        

    def pantallaSacarMoto (self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Pagina de ticketes salida moto
        page_ticketsSalidaMoto = QWidget()
        #layout de el registro de los tickets
        layout_ticketsSalidaMotos = QGridLayout()
        #------------------------Salida de motos------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_tickets = QLabel('REGISTRAR SALIDA MOTO')
        titulo_tickets.setStyleSheet(TITLE_STYLE_30_GRAY_BOLD)
        layout_ticketsSalidaMotos.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINE_STYLE_WHITE)
        layout_ticketsSalidaMotos.addWidget(linea_horizontal1, 1, 0, 1, 7)
        #-----Busqueda----
        # Crear el label "Codigo" y la textbox
        label_codigo = QLabel('Codigo:')
        label_codigo.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_codigo, 2, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box codigo
        self.textboxCodigoSacarMoto = QLineEdit()
        self.textboxCodigoSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxCodigoSacarMoto.setValidator(QIntValidator())
        layout_ticketsSalidaMotos.addWidget(self.textboxCodigoSacarMoto, 2, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        #-----
        # Crear el label "Placa" y la textbox
        label_placa = QLabel('Placa:')
        label_placa.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_placa, 3, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box placa
        self.textboxPlacaSacarMoto = QLineEdit()
        self.textboxPlacaSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget(self.textboxPlacaSacarMoto, 3, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxPlacaSacarMoto.textChanged.connect(lambda:  self.textboxPlacaSacarMoto.setText( self.textboxPlacaSacarMoto.text().upper()))
        #----
        # Crea un boton para buscar
        boton_buscar = QPushButton('Buscar')
        boton_buscar.setStyleSheet(BUTTON_STYLE_TICKETS_PRIMARY)
        layout_ticketsSalidaMotos.addWidget(boton_buscar, 2, 5, 2, 2,
                                alignment=Qt.AlignCenter| Qt.AlignHCenter)
        boton_buscar.clicked.connect(lambda: [
            self.cargarBusquedaSalidaMoto(),
        ])
#----Mostrar---
    #---Fila 1
        # Crear el label "Casillero" y la textbox
        label_casillero = QLabel('Casillero')
        label_casillero.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_casillero, 4, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box casillero
        self.textboxCasilleroSacarMoto = QLineEdit()
        self.textboxCasilleroSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget( self.textboxCasilleroSacarMoto, 5, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxCasilleroSacarMoto.setReadOnly(True)
        # Crear el label "Cascos" y la textbox
        label_cascos = QLabel('Cascos')
        label_cascos.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_cascos, 4, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box Cascos
        self.textboxCascosSacarMoto = QLineEdit()
        self.textboxCascosSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget(self.textboxCascosSacarMoto, 5, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxCascosSacarMoto.setReadOnly(True)
     #---Fila 2
        # Crear el label "Fecha ingreso" y la textbox
        label_FIngreso = QLabel('Fecha ingreso')
        label_FIngreso.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_FIngreso, 6, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box casillero
        self.textboxFIngresoSacarMoto = QLineEdit()
        self.textboxFIngresoSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget(self.textboxFIngresoSacarMoto, 7, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxFIngresoSacarMoto.setReadOnly(True)
        self.textboxFIngresoSacarMoto.textChanged.connect(self._actualizarEstadoBotonMotoSalida)
        # Crear el label "Hora ingreso" y la textbox
        label_HIngreso = QLabel('Hora ingreso')
        label_HIngreso.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_HIngreso, 6, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box Cascos
        self.textboxHIngresoSacarMoto = QLineEdit()
        self.textboxHIngresoSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget(self.textboxHIngresoSacarMoto, 7, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxHIngresoSacarMoto.setReadOnly(True)
    #---Fila 3
        # Crear el label "Fecha salida" y la textbox
        label_FSalida= QLabel('Fecha salida')
        label_FSalida.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_FSalida, 8, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box Fecha de salida
        self.textboxFSalidaSacarMoto = QLineEdit()
        self.textboxFSalidaSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget(self.textboxFSalidaSacarMoto, 9, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxFSalidaSacarMoto.setReadOnly(True)
        # Crear el label "Hora salida" y la textbox
        label_HSalida = QLabel('Hora salida')
        label_HSalida.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_HSalida, 8, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box Hoira salida
        self.textboxHSalidaSacarMoto = QLineEdit()
        self.textboxHSalidaSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget(self.textboxHSalidaSacarMoto, 9, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxHSalidaSacarMoto.setReadOnly(True)
    #---Fila 4
        # Crear el label "Pagado por" y la textbox
        label_PagadoPor= QLabel('Pagado por')
        label_PagadoPor.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_PagadoPor, 10, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box casillero
        self.textboxPagadoPorSacarMoto = QLineEdit()
        self.textboxPagadoPorSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget(self.textboxPagadoPorSacarMoto, 11, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxPagadoPorSacarMoto.setReadOnly(True)
        # Crear el label "Tiempo total" y la textbox
        label_TiempoTotal = QLabel('Tiempo total')
        label_TiempoTotal.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_TiempoTotal, 10, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box tiempo total
        self.textboxTiempoTotalSacarMoto = QLineEdit()
        self.textboxTiempoTotalSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget(self.textboxTiempoTotalSacarMoto, 11, 3, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxTiempoTotalSacarMoto.setReadOnly(True)
#----Facturar
        # Crear el label "Total a pagar" y la textbox
        label_TotalAPagar = QLabel('Total a pagar')
        label_TotalAPagar.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSalidaMotos.addWidget(label_TotalAPagar, 7, 5, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        # Text box Cascos
        self.textboxTotalAPagarSacarMoto = QLineEdit()
        self.textboxTotalAPagarSacarMoto.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSalidaMotos.addWidget(self.textboxTotalAPagarSacarMoto, 8, 5, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        self.textboxTotalAPagarSacarMoto.setReadOnly(True)
        # Crea un boton para facturar
        self.boton_facturar = QPushButton('Facturar')
        self.boton_facturar.setStyleSheet(BUTTON_STYLE_TICKETS_DISABLED)
        self._set_boton_interactivo(self.boton_facturar, False)
        # Conectar el botón de imprimir a la función registrarMoto
        self.boton_facturar.clicked.connect(lambda: [
            db_connection.registrarSalidaMoto(
                self.textboxCodigoSacarMoto.text(),
                float(self.textboxTotalAPagarSacarMoto.text().replace("$", "").strip())
            ),
            generarTicketSalidaMoto(
                self.textboxFIngresoSacarMoto.text(),
                self.textboxFSalidaSacarMoto.text(),
                self.textboxHIngresoSacarMoto.text(),
                self.textboxHSalidaSacarMoto.text(),
                self.textboxTiempoTotalSacarMoto.text(),
                float(self.textboxTotalAPagarSacarMoto.text().replace("$", "").strip()),
                self.textboxPlacaSacarMoto.text(),
                self.textboxCasilleroSacarMoto.text()
            ),
            # Cambiar estado de OCUPADO a DISPONIBLE (solo si casillero > 0)
            db_connection.cambiarEstadoCasillero(
                self.textboxCasilleroSacarMoto.text(),
                "OCUPADO"  # Estado actual = OCUPADO, se cambiará a DISPONIBLE
            ) if (self.textboxCasilleroSacarMoto.text() and 
                  self.textboxCasilleroSacarMoto.text() != "0" and 
                  int(self.textboxCasilleroSacarMoto.text()) > 0) else None,
            # Limpiar campos
            self.textboxCodigoSacarMoto.clear(),
            self.textboxPlacaSacarMoto.clear(),
            self.textboxCasilleroSacarMoto.clear(),
            self.textboxCascosSacarMoto.clear(),
            self.textboxFIngresoSacarMoto.clear(),
            self.textboxHIngresoSacarMoto.clear(),
            self.textboxFSalidaSacarMoto.clear(),
            self.textboxHSalidaSacarMoto.clear(),
            self.textboxPagadoPorSacarMoto.clear(),
            self.textboxTiempoTotalSacarMoto.clear(),
            self.textboxTotalAPagarSacarMoto.clear(),
            # Emitir señales
            self.senalActualizarTablasCasilleros.emit(),
            self.senalActualizarTablaRegistroMotos.emit(),
            self.senalActualizarResumen.emit(),
            self._set_boton_interactivo(self.boton_facturar, False),
        ])

        layout_ticketsSalidaMotos.addWidget(self.boton_facturar, 9, 5, 1, 2,
                                alignment=Qt.AlignTop| Qt.AlignCenter)
        # Establecer las proporciones de las filas en la cuadricula
        layout_ticketsSalidaMotos.setRowStretch(0, 0)
        layout_ticketsSalidaMotos.setRowStretch(1, 1)
        layout_ticketsSalidaMotos.setRowStretch(2, 1)
        layout_ticketsSalidaMotos.setRowStretch(3, 1)
        layout_ticketsSalidaMotos.setRowStretch(4, 1)
        layout_ticketsSalidaMotos.setRowStretch(5, 1)
        layout_ticketsSalidaMotos.setRowStretch(6, 1)
        layout_ticketsSalidaMotos.setRowStretch(7, 1)  
        layout_ticketsSalidaMotos.setRowStretch(8, 1)
        layout_ticketsSalidaMotos.setRowStretch(9, 1)
        layout_ticketsSalidaMotos.setRowStretch(10, 1)
        layout_ticketsSalidaMotos.setRowStretch(11, 1)    
    
        #Se agrega el layout a la pagina
        page_ticketsSalidaMoto.setLayout(layout_ticketsSalidaMotos)
        #Se agrega al stack
        self.stacked_widgetTickets.addWidget(page_ticketsSalidaMoto)

    def pantallaIngresarFijo(self):
         # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Pagina de ticketes salida moto
        page_ticketsIngresoFijo = QWidget()
        #layout de el registro de los tickets
        layout_ticketsIngresoFijo = QGridLayout()
        #------------------------Ingreso fijos------------------------------------
        # Crear el título  y añadirlo a la sección izquierda
        titulo_tickets = QLabel('REGISTRAR INGRESO FIJO')
        titulo_tickets.setStyleSheet(TITLE_STYLE_30_GRAY_BOLD)
        layout_ticketsIngresoFijo.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINE_STYLE_WHITE)
        layout_ticketsIngresoFijo.addWidget(linea_horizontal1, 1, 0, 1, 7)
    #---Fila 1
        # Crear el label "Codigo" y la textbox
        label_codigo = QLabel('Codigo')
        label_codigo.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsIngresoFijo.addWidget(label_codigo, 2, 2, 1, 1)
        # Text box Codigo 
        self.textbox_codigoFijos = QLineEdit()
        self.textbox_codigoFijos.setStyleSheet(TEXTBOX_STYLE_30)
        self.textbox_codigoFijos.setReadOnly(True)
        layout_ticketsIngresoFijo.addWidget(self.textbox_codigoFijos, 2, 3, 1, 1, alignment=Qt.AlignCenter)
        self.actualizarCodigoFijos()
    #---Fila 2
        # Crear el label "Tipo" y la textbox
        label_tipo = QLabel('Tipo')
        label_tipo.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsIngresoFijo.addWidget(label_tipo, 3, 2, 1, 1, alignment=Qt.AlignCenter)
        # combobox box Tipo
        combobox_Tipo = QComboBox()
        combobox_Tipo.addItems(['Puesto', 'Carretilla', 'Otro'])
        combobox_Tipo.setStyleSheet(TEXTBOX_STYLE_40)
        layout_ticketsIngresoFijo.addWidget(combobox_Tipo, 3, 3, 1, 1, alignment=Qt.AlignCenter)
    #---Fila 3
        # Crear el label "Nota" y la textbox
        label_Nota = QLabel('Nota')
        label_Nota.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsIngresoFijo.addWidget(label_Nota, 4, 2, 1, 1, alignment=Qt.AlignCenter)
        # Text box Codigo
        self.textboxNotaFijoIngreso = QLineEdit()
        self.textboxNotaFijoIngreso.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsIngresoFijo.addWidget(self.textboxNotaFijoIngreso, 4, 3, 1, 1, alignment=Qt.AlignCenter)
        self.textboxNotaFijoIngreso.textChanged.connect(self._actualizarEstadoBotonFijoIngreso)
    #---Fila 4
        # Crear el label "Valor" y la textbox
        label_Valor = QLabel('Valor')
        label_Valor.setStyleSheet(LABEL_STYLE_40_WHITE)
        layout_ticketsIngresoFijo.addWidget(label_Valor, 5, 2, 1, 1, alignment=Qt.AlignCenter)
        # Text box Codigo
        self.textboxValorFijo = QLineEdit()
        self.textboxValorFijo.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxValorFijo.setValidator(QIntValidator()) # Valida que solo pueda ingresar enteros 
        self.textboxValorFijo.textChanged.connect(self._actualizarEstadoBotonFijoIngreso)
        layout_ticketsIngresoFijo.addWidget(self.textboxValorFijo, 5, 3, 1, 1, alignment=Qt.AlignCenter)
    #---Fila 5
        # Boton para imprimir
        self.botonImprimirFijo = QPushButton('Imprimir')
        self.botonImprimirFijo.setStyleSheet(BUTTON_STYLE_TICKETS_DISABLED)
        self._set_boton_interactivo(self.botonImprimirFijo, False)
        layout_ticketsIngresoFijo.addWidget(self.botonImprimirFijo, 6, 3, 1, 1,
                                alignment=Qt.AlignTop| Qt.AlignLeft)
        # Conectar el botón de imprimir a la función registrarMoto
        self.botonImprimirFijo.clicked.connect(lambda: [
         # Validaciones
            QMessageBox.warning(None, "Advertencia", "Debe ingresar todos los datos.") 
            if not self.textboxNotaFijoIngreso.text().strip() or not self.textboxValorFijo.text().strip() else  [
            db_connection.registrarFijo(
            combobox_Tipo.currentText(),
            self.textboxNotaFijoIngreso.text(),
            self.textboxValorFijo.text(),
        ),
        combobox_Tipo.setCurrentIndex(0),
        self.textboxNotaFijoIngreso.clear(),
        self.textboxValorFijo.clear(),
        self.textbox_codigoFijos.clear(),
        self.actualizarCodigoFijos(),
        self.senalActualizarTablaRegistroFijos.emit(),
            ]])
        layout_ticketsIngresoFijo.setRowStretch(0, 0)
        layout_ticketsIngresoFijo.setRowStretch(1, 1)
        layout_ticketsIngresoFijo.setRowStretch(2, 1)
        layout_ticketsIngresoFijo.setRowStretch(3, 1)
        layout_ticketsIngresoFijo.setRowStretch(4, 1)
        layout_ticketsIngresoFijo.setRowStretch(5, 1)
        layout_ticketsIngresoFijo.setRowStretch(6, 1)
        #Se agrega el layout a la pagina
        page_ticketsIngresoFijo.setLayout(layout_ticketsIngresoFijo)
        #Se agrega al stack
        self.stacked_widgetTickets.addWidget(page_ticketsIngresoFijo)

    def pantallaSacarFijo(self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Pagina de ticketes salida moto
        page_ticketsSacarFijo = QWidget()
        #layout de el registro de los tickets
        layout_ticketsSacarFijo = QGridLayout()
        #------------------------Salida de fijos------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_tickets = QLabel('REGISTRAR SALIDA FIJO')
        titulo_tickets.setStyleSheet(TITLE_STYLE_30_GRAY_BOLD)
        layout_ticketsSacarFijo.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINE_STYLE_WHITE)
        layout_ticketsSacarFijo.addWidget(linea_horizontal1, 0, 0, 1, 7, alignment=Qt.AlignBottom)
    #---Buscar
        # Crear el label "Codigo" y la textbox
        label_codigo = QLabel('Codigo')
        label_codigo.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSacarFijo.addWidget(label_codigo, 1, 1, 2, 1, alignment=Qt.AlignHCenter | Qt.AlignCenter)
        # Text box Codigo
        self.textboxCodigoFijo = QLineEdit()
        self.textboxCodigoFijo.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxCodigoFijo.setValidator(QIntValidator())
        layout_ticketsSacarFijo.addWidget(self.textboxCodigoFijo, 1, 2, 2, 2, alignment=Qt.AlignCenter)
        # Boton para buscar
        botonBuscarFijos = QPushButton('Buscar')
        botonBuscarFijos.setStyleSheet(BUTTON_STYLE_TICKETS_PRIMARY)
        botonBuscarFijos.clicked.connect(lambda: [
            self.cargarBusquedaSalidaFijo(),])
        layout_ticketsSacarFijo.addWidget(botonBuscarFijos, 1, 5, 2, 1,
                                alignment=Qt.AlignCenter)
    #---Mostrar
    #---Fila 1
        # Crear el label "Tipo" y la textbox
        label_Tipo = QLabel('Tipo')
        label_Tipo.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSacarFijo.addWidget(label_Tipo, 3, 1, 1, 1, alignment=Qt.AlignBottom| Qt.AlignHCenter)
        # Text box tipo
        self.textboxTipoFijos = QLineEdit()
        self.textboxTipoFijos.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSacarFijo.addWidget(self.textboxTipoFijos, 4, 1, 1, 1, alignment=Qt.AlignTop)
        self.textboxTipoFijos.setReadOnly(True)
        # Crear el label "Nota" y la textbox
        label_Nota = QLabel('Nota')
        label_Nota.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSacarFijo.addWidget(label_Nota, 3, 3, 1, 1, alignment=Qt.AlignBottom| Qt.AlignHCenter)
        # Text box Cascos
        self.textboxNotaFijos = QLineEdit()
        self.textboxNotaFijos.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSacarFijo.addWidget(self.textboxNotaFijos, 4, 3, 1, 1, alignment= Qt.AlignTop)
        self.textboxNotaFijos.setReadOnly(True)
     #---Fila 2
        # Crear el label "Fecha ingreso" y la textbox
        label_FIngreso = QLabel('Fecha ingreso')
        label_FIngreso.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSacarFijo.addWidget(label_FIngreso, 5, 1, 1, 1, alignment=Qt.AlignBottom| Qt.AlignHCenter)
        # Text box casillero
        self.textboxFIngresoFijos = QLineEdit()
        self.textboxFIngresoFijos.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSacarFijo.addWidget(self.textboxFIngresoFijos, 6, 1, 1, 1, alignment=Qt.AlignTop)
        self.textboxFIngresoFijos.setReadOnly(True)
        self.textboxFIngresoFijos.textChanged.connect(self._actualizarEstadoBotonFijoSalida)
        # Crear el label "Hora ingreso" y la textbox
        label_HIngreso = QLabel('Hora ingreso')
        label_HIngreso.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSacarFijo.addWidget(label_HIngreso, 5, 3, 1, 1, alignment=Qt.AlignBottom| Qt.AlignHCenter)
        # Text box Cascos
        self.textboxHIngresoFijos = QLineEdit()
        self.textboxHIngresoFijos.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSacarFijo.addWidget(self.textboxHIngresoFijos, 6, 3, 1, 1, alignment= Qt.AlignTop)
        self.textboxHIngresoFijos.setReadOnly(True)
    #---Fila 3
        # Crear el label "Fecha salida" y la textbox
        label_FSalida= QLabel('Fecha salida')
        label_FSalida.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSacarFijo.addWidget(label_FSalida, 7, 1, 1, 1, alignment=Qt.AlignBottom| Qt.AlignHCenter)
        # Text box casillero
        self.textboxFSalidaFijos = QLineEdit()
        self.textboxFSalidaFijos.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSacarFijo.addWidget(self.textboxFSalidaFijos, 8, 1, 1, 1, alignment=Qt.AlignTop)
        self.textboxFSalidaFijos.setReadOnly(True)
        # Crear el label "Hora salida" y la textbox
        label_HSalida = QLabel('Hora salida')
        label_HSalida.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSacarFijo.addWidget(label_HSalida, 7, 3, 1, 1, alignment=Qt.AlignBottom| Qt.AlignHCenter)
        # Text box Cascos
        self.textboxHSalidaFijos = QLineEdit()
        self.textboxHSalidaFijos.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSacarFijo.addWidget(self.textboxHSalidaFijos, 8, 3, 1, 1, alignment= Qt.AlignTop)
        self.textboxHSalidaFijos.setReadOnly(True)
    #---Fila 4
        # Crear el label "Tiempo total" y la textbox
        label_TiempoTotal = QLabel('Tiempo total')
        label_TiempoTotal.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSacarFijo.addWidget(label_TiempoTotal, 3, 5, 1, 1, alignment=Qt.AlignBottom| Qt.AlignHCenter)
        # Text box tiempo total
        self.textboxTiempoTotalFijos = QLineEdit()
        self.textboxTiempoTotalFijos.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSacarFijo.addWidget(self.textboxTiempoTotalFijos, 4, 5, 1, 1, alignment= Qt.AlignTop)
        self.textboxTiempoTotalFijos.setReadOnly(True)
        # Crear el label "Total a pagar" y la textbox
        label_TotalApagar= QLabel('Total a pagar')
        label_TotalApagar.setStyleSheet(LABEL_STYLE_30_WHITE)
        layout_ticketsSacarFijo.addWidget(label_TotalApagar, 5, 5, 1, 1, alignment=Qt.AlignBottom| Qt.AlignHCenter)
        # Text box total a pagar
        self.textboxTotalApagarFijos = QLineEdit()
        self.textboxTotalApagarFijos.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsSacarFijo.addWidget(self.textboxTotalApagarFijos, 6, 5, 1, 1, alignment=Qt.AlignTop)
        self.textboxTotalApagarFijos.setReadOnly(True)
        # Crea un boton para facturar
        self.botonfacturarFijos = QPushButton('Facturar')
        self.botonfacturarFijos.setStyleSheet(BUTTON_STYLE_TICKETS_DISABLED)
        self._set_boton_interactivo(self.botonfacturarFijos, False)
        # Conectar el botón de imprimir a la función registrarMoto
        self.botonfacturarFijos.clicked.connect(lambda: [
            db_connection.registrarSalidaFijo(
            self.textboxCodigoFijo.text()
        ),
        generarTicketSalidaFijo(self.textboxTipoFijos.text(),
                                self.textboxNotaFijos.text(),
                                self.textboxFIngresoFijos.text(),
                                self.textboxFSalidaFijos.text(),
                                self.textboxHIngresoFijos.text(),
                                self.textboxHSalidaFijos.text(),
                                self.textboxTiempoTotalFijos.text(),
                                self.textboxTotalApagarFijos.text()
                                ),
        self.textboxCodigoFijo.clear(),
        self.textboxTipoFijos.clear (),
        self.textboxNotaFijos.clear(),
        self.textboxFIngresoFijos.clear(),
        self.textboxHIngresoFijos.clear(),
        self.textboxFSalidaFijos.clear(),
        self.textboxHSalidaFijos.clear(),
        self.textboxTotalApagarFijos.clear(),
        self.textboxHIngresoFijos.clear(),
        self.textboxFSalidaFijos.clear(),
        self.textboxTiempoTotalFijos.clear(),
        self.senalActualizarTablaRegistroFijos.emit(),
        self.senalActualizarResumen.emit(),
        self._set_boton_interactivo(self.botonfacturarFijos, False)
    ])

        layout_ticketsSacarFijo.addWidget(self.botonfacturarFijos, 7, 5, 1, 1,
                                alignment=Qt.AlignTop| Qt.AlignHCenter)
        # Establecer las proporciones de las filas en la cuadricula
        layout_ticketsSacarFijo.setRowStretch(0, 0)
        layout_ticketsSacarFijo.setRowStretch(1, 1)
        layout_ticketsSacarFijo.setRowStretch(2, 1)
        layout_ticketsSacarFijo.setRowStretch(3, 1)
        layout_ticketsSacarFijo.setRowStretch(4, 1)
        layout_ticketsSacarFijo.setRowStretch(5, 1)
        layout_ticketsSacarFijo.setRowStretch(6, 1)
        layout_ticketsSacarFijo.setRowStretch(7, 1)  
        layout_ticketsSacarFijo.setRowStretch(8, 1)

        #Se agrega el layout a la pagina
        page_ticketsSacarFijo.setLayout(layout_ticketsSacarFijo)
        #Se agrega al stack
        self.stacked_widgetTickets.addWidget(page_ticketsSacarFijo)

    def pantallaIngresarMensualidad(self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Pagina de ticketes salida moto
        page_ticketsIngresarMensualidad = QWidget()
        #layout de el registro de los tickets
        layout_ticketsIngresarMensualidad = QGridLayout()
        #------------------------Salida de fijos------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_tickets = QLabel('REGISTRAR MENSUALIDAD')
        titulo_tickets.setStyleSheet(TITLE_STYLE_30_GRAY_BOLD)
        layout_ticketsIngresarMensualidad.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINE_STYLE_WHITE)
        layout_ticketsIngresarMensualidad.addWidget(linea_horizontal1, 1, 0, 1, 7)

        #Placa
        titulo_Placa = QLabel('PLACA')
        titulo_Placa .setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsIngresarMensualidad.addWidget(titulo_Placa,2, 2, 1, 1, alignment= Qt.AlignCenter)
        
        self.textboxPlacaMensualidad = QLineEdit()
        self.textboxPlacaMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsIngresarMensualidad.addWidget(self.textboxPlacaMensualidad, 2, 3, 1, 1, alignment=Qt.AlignCenter)
        self.textboxPlacaMensualidad.textChanged.connect(lambda: self.textboxPlacaMensualidad.setText(self.textboxPlacaMensualidad.text().upper()))
        self.textboxPlacaMensualidad.textChanged.connect(self._actualizarEstadoBotonMensualidadIngreso)

        #Nombre
        titulo_Nombre = QLabel('NOMBRE')
        titulo_Nombre .setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsIngresarMensualidad.addWidget(titulo_Nombre  , 3, 2, 1, 1, alignment= Qt.AlignCenter|Qt.AlignLeft)
        
        self.textboxNombreMensualidad = QLineEdit()
        self.textboxNombreMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsIngresarMensualidad.addWidget(self.textboxNombreMensualidad, 3, 3, 1, 1, alignment=Qt.AlignCenter|Qt.AlignLeft)
        self.textboxNombreMensualidad.textChanged.connect(self._actualizarEstadoBotonMensualidadIngreso)

        #Telefono
        titulo_Telefono = QLabel('TELEFONO')
        titulo_Telefono .setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsIngresarMensualidad.addWidget(titulo_Telefono  ,4, 2, 1, 1, alignment= Qt.AlignCenter|Qt.AlignLeft)
        
        self.textboxTelefonoMensualidad = QLineEdit()
        self.textboxTelefonoMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsIngresarMensualidad.addWidget(self.textboxTelefonoMensualidad, 4, 3, 1, 1, alignment=Qt.AlignCenter|Qt.AlignLeft)
        self.textboxTelefonoMensualidad.textChanged.connect(self._actualizarEstadoBotonMensualidadIngreso)
        #Mensualidades Vigentes
        titulo_MensualidadesVigentes = QLabel('Mensualidades Vigentes')
        # Centrar el texto en el QLabel
        titulo_MensualidadesVigentes .setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsIngresarMensualidad.addWidget(titulo_MensualidadesVigentes  ,6, 0, 1, 3, alignment= Qt.AlignCenter)
        
        self.textbox_MensualidadesVigentes = QLineEdit()
        self.textbox_MensualidadesVigentes.setStyleSheet(TEXTBOX_STYLE_30)
        self.textbox_MensualidadesVigentes.setFixedWidth(60)
        self.textbox_MensualidadesVigentes.setReadOnly(True)
        layout_ticketsIngresarMensualidad.addWidget(self.textbox_MensualidadesVigentes, 6, 3, 1, 1, alignment=Qt.AlignCenter |Qt.AlignLeft)
        self.actualizarMensualidadesVigentes()
        #Boton Imprimir
        self.botonImprimirMensualidad = QPushButton('IMPRIMIR')
        self.botonImprimirMensualidad.setStyleSheet("""
            QPushButton {
                color: White;
                background-color: #222125;
                font-size: 35px;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #666666;
            }
            QPushButton:disabled:hover {
                background-color: #3a3a3a;
                color: #666666;
                border: none;
            }
            QPushButton:disabled:pressed {
                background-color: #3a3a3a;
                color: #666666;
                border: none;
            }
        """)
        self._set_boton_interactivo(self.botonImprimirMensualidad, False)
        layout_ticketsIngresarMensualidad.addWidget(self.botonImprimirMensualidad,5, 0, 1, 7,alignment=Qt.AlignCenter)
        # Conectar el botón de imprimir a la función registrarMoto
        self.botonImprimirMensualidad.clicked.connect(lambda: [
             QMessageBox.warning(None, "Advertencia", "Debe ingresar todos los datos.") 
            if not self.textboxPlacaMensualidad.text().strip() or not self.textboxNombreMensualidad.text().strip() or not self.textboxTelefonoMensualidad.text().strip() else
                QMessageBox.warning(None, "Advertencia", "Esta placa ya esta registrada en mensualidades.") 
            if db_connection.validarPlacaActivaMensualidad(self.textboxPlacaMensualidad.text()) else [
            db_connection.registrarMensualidad(
            self.textboxPlacaMensualidad.text(),
            self.textboxNombreMensualidad.text(),
            self.textboxTelefonoMensualidad.text(),
        ),
        self.textboxPlacaMensualidad.clear(),
        self.textboxNombreMensualidad.clear(),
        self.textboxTelefonoMensualidad.clear(),
        self.senalActualizarTablaRegistroMensualidades.emit(),#Se emite la señal para actualizar la tabla de mensualidades
        self.senalActualizarResumen.emit(),
        self.actualizarMensualidadesVigentes()
    ]])
        # Establecer las proporciones de las filas en la cuadricula
        layout_ticketsIngresarMensualidad.setRowStretch(0, 0)
        layout_ticketsIngresarMensualidad.setRowStretch(1, 1)
        layout_ticketsIngresarMensualidad.setRowStretch(2, 1)
        layout_ticketsIngresarMensualidad.setRowStretch(3, 1)
        layout_ticketsIngresarMensualidad.setRowStretch(4, 1)
        layout_ticketsIngresarMensualidad.setRowStretch(5, 1)
        layout_ticketsIngresarMensualidad.setRowStretch(6, 1)
        #Se agrega el layout a la pagina
        page_ticketsIngresarMensualidad.setLayout(layout_ticketsIngresarMensualidad)
        #Se agrega al stack
        self.stacked_widgetTickets.addWidget(page_ticketsIngresarMensualidad)
        
    def pantallaRenovarMensualidad(self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Pagina de ticketes salida moto
        page_ticketsRenovarMensualidad = QWidget()
        #layout de el registro de los tickets
        layout_ticketsRenovarMensualidad = QGridLayout()
        #------------------------Salida de fijos------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_tickets = QLabel('RENOVAR MENSUALIDAD')
        titulo_tickets.setStyleSheet(TITLE_STYLE_30_GRAY_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINE_STYLE_WHITE)
        layout_ticketsRenovarMensualidad.addWidget(linea_horizontal1, 1, 0, 1, 7)

        #Codigo
        titulo_Codigo = QLabel('CODIGO')
        titulo_Codigo.setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_Codigo  , 2, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxCodigoRenovarMensualidad = QLineEdit()
        self.textboxCodigoRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxCodigoRenovarMensualidad, 2, 3, 1, 2, alignment=Qt.AlignHCenter |Qt.AlignCenter)
        #Placa
        titulo_Placa = QLabel('PLACA')
        titulo_Placa .setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_Placa  , 3, 1, 1, 2, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxPlacaRenovarMensualidad = QLineEdit()
        self.textboxPlacaRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxPlacaRenovarMensualidad, 3, 3, 1, 2, alignment=Qt.AlignHCenter |Qt.AlignCenter)

        #Boton Buscar
        self.botonBuscarRenovarMensualidad = QPushButton('BUSCAR')
        self.botonBuscarRenovarMensualidad.setStyleSheet(BUTTON_STYLE_DARK_25_10_20)
        layout_ticketsRenovarMensualidad.addWidget(self.botonBuscarRenovarMensualidad, 2, 5, 2, 2,alignment=Qt.AlignHCenter|Qt.AlignCenter)
        self.botonBuscarRenovarMensualidad.clicked.connect(lambda: [
        self.cargarBusquedaRenovarMensualidad(),
    ])
        #Nombre
        titulo_Nombre = QLabel('NOMBRE')
        titulo_Nombre.setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_Nombre  , 4, 1, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxNombreRenovarMensualidad = QLineEdit()
        self.textboxNombreRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxNombreRenovarMensualidad.setReadOnly(True)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxNombreRenovarMensualidad, 5, 1, 1, 1, alignment=Qt.AlignHCenter |Qt.AlignCenter)
        
        #Fecha de Ingreso
        titulo_FechaIngreso = QLabel('FECHA\nINGRESO')
        # Centrar el texto horizontal y verticalmente
        titulo_FechaIngreso.setAlignment(Qt.AlignCenter)
        titulo_FechaIngreso.setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_FechaIngreso  ,6, 1, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxFechaIngresoRenovarMensualidad = QLineEdit()
        self.textboxFechaIngresoRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxFechaIngresoRenovarMensualidad.setReadOnly(True)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxFechaIngresoRenovarMensualidad, 7, 1, 1, 1, alignment=Qt.AlignHCenter |Qt.AlignCenter)
        self.textboxFechaIngresoRenovarMensualidad.textChanged.connect(self._actualizarEstadoBotonRenovarMensualidad)

        #Fecha U Pago
        titulo_FechaUPago = QLabel('FECHA\nU.PAGO')
        titulo_FechaUPago.setAlignment(Qt.AlignCenter)
        titulo_FechaUPago.setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_FechaUPago  , 8, 1, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxFechaUPagoRenovarMensualidad = QLineEdit()
        self.textboxFechaUPagoRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxFechaUPagoRenovarMensualidad.setReadOnly(True)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxFechaUPagoRenovarMensualidad, 9, 1, 1, 1, alignment=Qt.AlignHCenter |Qt.AlignCenter)
        
        #Fecha Renovacion
        titulo_FechaRenovacion = QLabel('FECHA RENOVACIÓN')
        titulo_FechaRenovacion.setAlignment(Qt.AlignCenter)
        titulo_FechaRenovacion.setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_FechaRenovacion  , 10, 1, 1, 3, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxFechaRenovacionRenovarMensualidad = QLineEdit()
        self.textboxFechaRenovacionRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxFechaRenovacionRenovarMensualidad.setReadOnly(True)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxFechaRenovacionRenovarMensualidad, 11, 1, 1, 3, alignment=Qt.AlignCenter |Qt.AlignHCenter)  

        #Telefono
        titulo_Telefono = QLabel('TELEFONO')
        titulo_Telefono.setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_Telefono  , 4, 3, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxTelefonoRenovarMensualidad = QLineEdit()
        self.textboxTelefonoRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxTelefonoRenovarMensualidad.setReadOnly(True)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxTelefonoRenovarMensualidad, 5, 3, 1, 1, alignment=Qt.AlignHCenter |Qt.AlignCenter)

        #Hora de Ingreso
        titulo_HoraIngreso = QLabel('HORA\nINGRESO')
        titulo_HoraIngreso.setAlignment(Qt.AlignCenter)
        titulo_HoraIngreso.setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_HoraIngreso  ,6, 3, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxHoraIngresoRenovarMensualidad = QLineEdit()
        self.textboxHoraIngresoRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxHoraIngresoRenovarMensualidad.setReadOnly(True)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxHoraIngresoRenovarMensualidad, 7, 3, 1, 1, alignment=Qt.AlignCenter |Qt.AlignHCenter)

        #Hora U Pago
        titulo_HoraUPago = QLabel('HORA\nU.PAGO')
        titulo_HoraUPago.setAlignment(Qt.AlignCenter)
        titulo_HoraUPago.setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_HoraUPago  , 8, 3, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxHoraUPagoRenovarMensualidad = QLineEdit()
        self.textboxHoraUPagoRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxHoraUPagoRenovarMensualidad.setReadOnly(True)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxHoraUPagoRenovarMensualidad, 9, 3, 1, 1, alignment=Qt.AlignCenter |Qt.AlignHCenter)

        #Total a pagar
        titulo_TotalAPagar = QLabel('TOTAL A PAGAR')
        titulo_TotalAPagar.setStyleSheet(TITLE_STYLE_30_WHITE_BOLD)
        layout_ticketsRenovarMensualidad.addWidget(titulo_TotalAPagar  , 6, 5, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        self.textboxTotalAPagarRenovarMensualidad = QLineEdit()
        self.textboxTotalAPagarRenovarMensualidad.setStyleSheet(TEXTBOX_STYLE_30)
        self.textboxTotalAPagarRenovarMensualidad.setReadOnly(True)
        layout_ticketsRenovarMensualidad.addWidget(self.textboxTotalAPagarRenovarMensualidad, 7, 5, 1, 1, alignment=Qt.AlignCenter |Qt.AlignHCenter)
        
        #Boton Renovar
        self.botonRenovarMensualidad = QPushButton('RENOVAR')
        self.botonRenovarMensualidad.setStyleSheet("""
            QPushButton {
                color: White;
                background-color: #222125;
                font-size: 30px;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #666666;
            }
            QPushButton:disabled:hover {
                background-color: #3a3a3a;
                color: #666666;
                border: none;
            }
            QPushButton:disabled:pressed {
                background-color: #3a3a3a;
                color: #666666;
                border: none;
            }
        """)
        # Conectar el botón de imprimir a la función registrarMoto
        self.botonRenovarMensualidad.clicked.connect(lambda: [
            db_connection.registrarRenovarMensualidad(
            self.textboxCodigoRenovarMensualidad.text(),
            self.textboxFechaRenovacionRenovarMensualidad.text()
        ),
        self.textboxCodigoRenovarMensualidad.clear(),
        self.textboxPlacaRenovarMensualidad.clear (),
        self.textboxNombreRenovarMensualidad.clear(),
        self.textboxFechaIngresoRenovarMensualidad.clear(),
        self.textboxFechaUPagoRenovarMensualidad.clear(),
        self.textboxFechaRenovacionRenovarMensualidad.clear(),
        self.textboxTelefonoRenovarMensualidad.clear(),
        self.textboxHoraIngresoRenovarMensualidad.clear(),
        self.textboxHoraUPagoRenovarMensualidad.clear(),
        self.textboxTotalAPagarRenovarMensualidad.clear(),
        self.senalActualizarTablaRegistroMensualidades.emit(),
        self._set_boton_interactivo(self.botonRenovarMensualidad, False),
        self.senalActualizarResumen.emit(),
        self.senalActualizarTextboxMensualidadesVigentes.emit()
    ])
        
        
        
        layout_ticketsRenovarMensualidad.addWidget(self.botonRenovarMensualidad,8, 5, 1, 1, alignment=Qt.AlignCenter |Qt.AlignHCenter)
        self._set_boton_interactivo(self.botonRenovarMensualidad, False)
        # Establecer las proporciones de las filas en la cuadricula
        layout_ticketsRenovarMensualidad.setRowStretch(0, 0)
        layout_ticketsRenovarMensualidad.setRowStretch(1, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(2, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(3, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(4, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(5, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(6, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(7, 1)  
        layout_ticketsRenovarMensualidad.setRowStretch(8, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(9, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(10, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(11, 1)
        #Se agrega el layout a la pagina
        page_ticketsRenovarMensualidad.setLayout(layout_ticketsRenovarMensualidad)
        #Se agrega al stack
        self.stacked_widgetTickets.addWidget(page_ticketsRenovarMensualidad)
    def actualizarCodigoFijos (self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        self.textbox_codigoFijos.setText(str(db_connection.obtenerSiguienteIDFijos()))
