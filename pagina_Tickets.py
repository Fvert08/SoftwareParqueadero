from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
from DatabaseConnection import DatabaseConnection
from config import DB_CONFIG
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from datetime import datetime
from TicketSalidaMotos import generarTicketSalidaMoto
class PaginaTickets(QWidget):
    senalActualizarTablasCasilleros= pyqtSignal()
    senalActualizarTablaRegistroMotos = pyqtSignal()
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

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
                self.boton_facturar.setDisabled(True)#Deshabilitar botón para imprimir

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
                cobroPorHora= 1000 #Cobro por hora del parqueadero
                cobroPorDia = 5000 #Cobro ppr dia del parqueadero
                #-------------------------------------------------------------------
                if (minutos or segundos)>0: #Si Se lleva a subre pasar un segundo o un minuto de más se cobrará una hora completa
                    horas+=1
                if str(datosBusquedaSalidaMoto['Tipo']) == "Dia":
                    self.totalAPagarSacarMoto = cobroPorDia
                else:
                    self.totalAPagarSacarMoto = horas*cobroPorHora
                self.textboxTotalAPagarSacarMoto.setText(f"${str(self.totalAPagarSacarMoto)}")
                self.boton_facturar.setEnabled(True)# Habilitar Botón para imprimir
        else:
            print("No se encontraron registros")
    def actualizarTextboxCasilleros (self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        self.textbox_casillero.setText(str(db_connection.casilleroAsignado(1))),
        self.textbox_casillerosDis.setText(str(db_connection.casillerosDisponibles(1)))
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
        linea_vertical.setStyleSheet("color: #FFFFFF;")
        layout_ticketsmenu.addWidget(linea_vertical, 0, 0, 8, 1)
        # Crear la sección derecha con el título "Menú"
        titulo_menu = QLabel('Menú')
        titulo_menu.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_ticketsmenu.addWidget(titulo_menu, 0, 1, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)
        linea_horizontal2 = QFrame()
        linea_horizontal2.setFrameShape(QFrame.HLine)
        linea_horizontal2.setLineWidth(1)
        linea_horizontal2.setStyleSheet("color: #FFFFFF;")
        layout_ticketsmenu.addWidget(linea_horizontal2, 0, 1, 1, 2, alignment=Qt.AlignBottom)

        layout_ticketsmenu.setRowStretch(0, 0)
        layout_ticketsmenu.setRowStretch(1, 1)
        layout_ticketsmenu.setRowStretch(2, 1)
        layout_ticketsmenu.setRowStretch(3, 1)
        layout_ticketsmenu.setRowStretch(4, 1)
        layout_ticketsmenu.setRowStretch(5, 1)
        layout_ticketsmenu.setRowStretch(6, 1)

        # Crea un boton para ingresar a generar ticket ingresar moto
        boton_IngresarM = QPushButton()
        boton_IngresarM.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        boton_IngresarM.setIcon(QIcon('IngresoMoto.png'))  # Establecer el icono
        boton_IngresarM.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarM, 1, 1, 1, 1, alignment=Qt.AlignTop | Qt.AlignRight | Qt.AlignCenter)
        boton_IngresarM.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(0))


        # Crea un boton para ingresar a generar ticket sacar moto
        boton_SacarM = QPushButton()
        boton_SacarM.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        boton_SacarM.setIcon(QIcon('SalidaMoto.png'))  # Establecer el icono
        boton_SacarM.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarM, 1, 2, 1, 1, alignment=Qt.AlignTop | Qt.AlignLeft | Qt.AlignCenter)
        boton_SacarM.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(1))


        # Crea un boton para ingresar a generar ticket ingresar Fijo
        boton_IngresarF = QPushButton()
        boton_IngresarF.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        boton_IngresarF.setIcon(QIcon('IngresoFijo.png'))  # Establecer el icono
        boton_IngresarF.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarF, 2, 1, 1, 1, alignment=Qt.AlignTop | Qt.AlignRight | Qt.AlignCenter)
        boton_IngresarF.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(2))

        # Crea un boton para ingresar a generar ticket sacar Fijo
        boton_SacarF = QPushButton()
        boton_SacarF.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        boton_SacarF.setIcon(QIcon('SalidaFijo.png'))  # Establecer el icono
        boton_SacarF.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarF, 2, 2, 1, 1, alignment=Qt.AlignTop | Qt.AlignLeft | Qt.AlignCenter)
        boton_SacarF.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(3))
        
        #Crea un boton para ingresar a generar ticket ingresar Mensualidad
        boton_IngresarMensualidad = QPushButton()
        boton_IngresarMensualidad.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_IngresarMensualidad.setIcon(QIcon('Mesingreso.png'))  # Establecer el icono
        boton_IngresarMensualidad.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarMensualidad, 3, 1, 1, 1, alignment=Qt.AlignTop | Qt.AlignRight | Qt.AlignCenter)
        boton_IngresarMensualidad.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(4))

        #Crea un boton para ingresar a generar ticket sacar Mensualidad
        boton_SacarMensualidad = QPushButton()
        boton_SacarMensualidad.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_SacarMensualidad.setIcon(QIcon('Mesrenovar.png'))  # Establecer el icono
        boton_SacarMensualidad.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarMensualidad,   3, 2, 1, 1, alignment=Qt.AlignTop | Qt.AlignLeft | Qt.AlignCenter)
        boton_SacarMensualidad.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(5))

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
        titulo_tickets.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_ticketsIngresoMotos.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_ticketsIngresoMotos.addWidget(linea_horizontal1, 0, 0, 1, 7, alignment=Qt.AlignBottom)

        # Crear el label "Placa" y la textbox
        label_placa = QLabel('Placa:')
        label_placa.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsIngresoMotos.addWidget(label_placa, 1, 2, 1, 1, alignment=Qt.AlignCenter | Qt.AlignRight)

        textbox_placa = QLineEdit()
        textbox_placa.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_placa.setFixedWidth(240)
        layout_ticketsIngresoMotos.addWidget(textbox_placa, 1, 3, 1, 1, alignment=Qt.AlignCenter | Qt.AlignLeft)

        # Crear el label "Cascos" y el combobox
        label_cascos = QLabel('Cascos:')
        label_cascos.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsIngresoMotos.addWidget(label_cascos, 2, 2, 1, 1, alignment=Qt.AlignCenter | Qt.AlignRight)

        combobox_cascos = QComboBox()
        combobox_cascos.addItems(['0', '1', '2'])
        combobox_cascos.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 40px;")
        combobox_cascos.setFixedWidth(60)
        layout_ticketsIngresoMotos.addWidget(combobox_cascos, 2, 3, 1, 1, alignment=Qt.AlignCenter | Qt.AlignLeft)

        # Crear el label "Tiempo" y el combobox
        label_Tiempo = QLabel('Tiempo:')
        label_Tiempo.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsIngresoMotos.addWidget(label_Tiempo, 3, 2, 1, 1, alignment=Qt.AlignCenter | Qt.AlignRight)

        combobox_Tiempo = QComboBox()
        combobox_Tiempo.addItems(['Hora', 'Dia'])
        combobox_Tiempo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 40px;")
        combobox_Tiempo.setFixedWidth(120)
        layout_ticketsIngresoMotos.addWidget(combobox_Tiempo, 3, 3, 1, 1, alignment=Qt.AlignCenter | Qt.AlignLeft)

        # Crea una checkbox para confirmar que se eligio dia o mes  en "combobox_Tiempo"
        checkbox_opcion = QCheckBox('Confirmar', page_tickets)
        checkbox_opcion.setStyleSheet("color: #FFFFFF; font-size: 20px;")
        checkbox_opcion.setChecked(False)  # Opcional: Puedes establecer si la casilla está marcada por defecto o no
        layout_ticketsIngresoMotos.addWidget(checkbox_opcion, 3, 3, 1, 1,
                                alignment= Qt.AlignCenter |Qt.AlignRight)
        # Crear el label "Casillero" y el combobox
        label_casillero = QLabel('Casillero:', page_tickets)
        label_casillero.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsIngresoMotos.addWidget(label_casillero, 4, 2, 1, 1,
                                alignment=Qt.AlignCenter | Qt.AlignRight)  # Alineamiento arriba y a la izquierda
        self.textbox_casillero = QLineEdit(page_tickets)
        self.textbox_casillero.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        self.textbox_casillero.setReadOnly(True)
        self.textbox_casillero.setFixedWidth(100)  # Establecer el ancho fijo
        self.textbox_casillero.setFixedHeight(50)
        self.textbox_casillero.setText ("1")
        layout_ticketsIngresoMotos.addWidget(self.textbox_casillero, 4, 3, 1, 1,
                                alignment=Qt.AlignCenter | Qt.AlignLeft)  # Alineamiento arriba y a la izquierda
        self.textbox_casillero.setText(str(db_connection.casilleroAsignado(1)))

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
        """)
        layout_ticketsIngresoMotos.addWidget(boton_cambiarcasillero, 4, 3, 1, 1,
                                alignment=Qt.AlignCenter | Qt.AlignRight)

        # Crear el label "Casilleros disponibles" y el combobox
        label_casillerosDis = QLabel('Casilleros disponibles:', page_tickets)
        label_casillerosDis.setStyleSheet("color: #FFFFFF;font-size: 30px;")
        layout_ticketsIngresoMotos.addWidget(label_casillerosDis, 5, 2, 1, 1,
                                alignment=Qt.AlignCenter | Qt.AlignRight)  # Alineamiento arriba y a la izquierda
        #Crear Textbox "Casilleros disponibles" 
        self.textbox_casillerosDis = QLineEdit(page_tickets)
        self.textbox_casillerosDis.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        self.textbox_casillerosDis.setReadOnly(True)
        self.textbox_casillerosDis.setFixedWidth(70)  # Establecer el ancho fijo
        self.textbox_casillerosDis.setFixedHeight(50)
        self.textbox_casillerosDis.setText(str(db_connection.casillerosDisponibles(1)))
        layout_ticketsIngresoMotos.addWidget(self.textbox_casillerosDis, 5, 3, 1, 1,
                                alignment=Qt.AlignCenter | Qt.AlignLeft)  # Alineamiento arriba y a la izquierda
        # Crea un boton para Imprimir
        boton_imprimir = QPushButton('Imprimir', page_tickets)
        boton_imprimir.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        layout_ticketsIngresoMotos.addWidget(boton_imprimir, 6, 3, 1, 1,
                                alignment=Qt.AlignTop | Qt.AlignLeft)
        # Conectar el botón de imprimir a la función registrarMoto
        boton_imprimir.clicked.connect(lambda: [
            db_connection.registrarMoto(
            textbox_placa.text(),
            combobox_cascos.currentText(),
            combobox_Tiempo.currentText(),
            self.textbox_casillerosDis.text()
        ),
        textbox_placa.clear(),
        combobox_cascos.setCurrentIndex(0),
        combobox_Tiempo.setCurrentIndex(0),
        db_connection.cambiarEstadoCasillero(self.textbox_casillero.text(),"DISPONIBLE"),
        self.actualizarTextboxCasilleros(),
        self.senalActualizarTablasCasilleros.emit(),
        self.senalActualizarTablaRegistroMotos.emit()
    ])
        # Establecer las proporciones de las filas en la cuadricula
        layout_ticketsIngresoMotos.setRowStretch(0, 0)
        layout_ticketsIngresoMotos.setRowStretch(1, 1)
        layout_ticketsIngresoMotos.setRowStretch(2, 1)
        layout_ticketsIngresoMotos.setRowStretch(3, 1)
        layout_ticketsIngresoMotos.setRowStretch(4, 1)
        layout_ticketsIngresoMotos.setRowStretch(5, 1)
        layout_ticketsIngresoMotos.setRowStretch(6, 1)
        #Se agrega el layout a la pagina
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
        titulo_tickets.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_ticketsSalidaMotos.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_ticketsSalidaMotos.addWidget(linea_horizontal1, 0, 0, 1, 7, alignment=Qt.AlignBottom)
        #-----Busqueda----
        # Crear el label "Codigo" y la textbox
        label_codigo = QLabel('Codigo:')
        label_codigo.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSalidaMotos.addWidget(label_codigo, 1, 2, 1, 1, alignment=Qt.AlignCenter | Qt.AlignRight)
        # Text box codigo
        self.textboxCodigoSacarMoto = QLineEdit()
        self.textboxCodigoSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        self.textboxCodigoSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxCodigoSacarMoto, 1, 3, 1, 1, alignment=Qt.AlignCenter | Qt.AlignLeft)
        #-----
        # Crear el label "Placa" y la textbox
        label_placa = QLabel('Placa:')
        label_placa.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSalidaMotos.addWidget(label_placa, 2, 2, 1, 1, alignment=Qt.AlignTop | Qt.AlignRight)
        # Text box codigo
        self.textboxPlacaSacarMoto = QLineEdit()
        self.textboxPlacaSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        self.textboxPlacaSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxPlacaSacarMoto, 2, 3, 1, 1, alignment=Qt.AlignTop| Qt.AlignLeft)
        #----
        # Crea un boton para buscar
        boton_buscar = QPushButton('Buscar')
        boton_buscar.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        layout_ticketsSalidaMotos.addWidget(boton_buscar, 1, 6, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignLeft)
        boton_buscar.clicked.connect(lambda: [
            self.cargarBusquedaSalidaMoto(),
            db_connection.cambiarEstadoCasillero(self.textboxCasilleroSacarMoto.text(),"OCUPADO"),
    ])
#----Mostrar---
    #---Fila 1
        # Crear el label "Casillero" y la textbox
        label_casillero = QLabel('Casillero')
        label_casillero.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_casillero, 3, 1, 1, 1, alignment=Qt.AlignTop)
        # Text box casillero
        self.textboxCasilleroSacarMoto = QLineEdit()
        self.textboxCasilleroSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        self.textboxCasilleroSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget( self.textboxCasilleroSacarMoto, 4, 1, 1, 1, alignment=Qt.AlignTop)
        self.textboxCasilleroSacarMoto.setReadOnly(True)
        # Crear el label "Cascos" y la textbox
        label_cascos = QLabel('Cascos')
        label_cascos.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_cascos, 3, 3, 1, 1, alignment=Qt.AlignTop)
        # Text box Cascos
        self.textboxCascosSacarMoto = QLineEdit()
        self.textboxCascosSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        self.textboxCascosSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxCascosSacarMoto, 4, 3, 1, 1, alignment= Qt.AlignTop)
        self.textboxCascosSacarMoto.setReadOnly(True)
     #---Fila 2
        # Crear el label "Fecha ingreso" y la textbox
        label_FIngreso = QLabel('Fecha ingreso')
        label_FIngreso.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_FIngreso, 5, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box casillero
        self.textboxFIngresoSacarMoto = QLineEdit()
        self.textboxFIngresoSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        self.textboxFIngresoSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxFIngresoSacarMoto, 6, 1, 1, 1, alignment=Qt.AlignTop)
        self.textboxFIngresoSacarMoto.setReadOnly(True)
        # Crear el label "Hora ingreso" y la textbox
        label_HIngreso = QLabel('Hora ingreso')
        label_HIngreso.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_HIngreso, 5, 3, 1, 2, alignment=Qt.AlignTop)
        # Text box Cascos
        self.textboxHIngresoSacarMoto = QLineEdit()
        self.textboxHIngresoSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        self.textboxHIngresoSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxHIngresoSacarMoto, 6, 3, 1, 1, alignment= Qt.AlignTop)
        self.textboxHIngresoSacarMoto.setReadOnly(True)
    #---Fila 3
        # Crear el label "Fecha salida" y la textbox
        label_FSalida= QLabel('Fecha salida')
        label_FSalida.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_FSalida, 7, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box Fecha de salida
        self.textboxFSalidaSacarMoto = QLineEdit()
        self.textboxFSalidaSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        self.textboxFSalidaSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxFSalidaSacarMoto, 8, 1, 1, 1, alignment=Qt.AlignTop)
        self.textboxFSalidaSacarMoto.setReadOnly(True)
        # Crear el label "Hora salida" y la textbox
        label_HSalida = QLabel('Hora salida')
        label_HSalida.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_HSalida, 7, 3, 1, 2, alignment=Qt.AlignTop)
        # Text box Hoira salida
        self.textboxHSalidaSacarMoto = QLineEdit()
        self.textboxHSalidaSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        self.textboxHSalidaSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxHSalidaSacarMoto, 8, 3, 1, 1, alignment= Qt.AlignTop)
        self.textboxHSalidaSacarMoto.setReadOnly(True)
    #---Fila 4
        # Crear el label "Pagado por" y la textbox
        label_PagadoPor= QLabel('Pagado por')
        label_PagadoPor.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_PagadoPor, 9, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box casillero
        self.textboxPagadoPorSacarMoto = QLineEdit()
        self.textboxPagadoPorSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        self.textboxPagadoPorSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxPagadoPorSacarMoto, 10, 1, 1, 1, alignment=Qt.AlignTop)
        self.textboxPagadoPorSacarMoto.setReadOnly(True)
        # Crear el label "Tiempo total" y la textbox
        label_TiempoTotal = QLabel('Tiempo total')
        label_TiempoTotal.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_TiempoTotal, 9, 3, 1, 2, alignment=Qt.AlignTop)
        # Text box tiempo total
        self.textboxTiempoTotalSacarMoto = QLineEdit()
        self.textboxTiempoTotalSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        self.textboxTiempoTotalSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxTiempoTotalSacarMoto, 10, 3, 1, 1, alignment= Qt.AlignTop)
        self.textboxTiempoTotalSacarMoto.setReadOnly(True)
#----Facturar
        # Crear el label "Total a pagar" y la textbox
        label_TotalAPagar = QLabel('Total a pagar')
        label_TotalAPagar.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_TotalAPagar, 6, 6, 1, 2, alignment=Qt.AlignTop| Qt.AlignCenter)
        # Text box Cascos
        self.textboxTotalAPagarSacarMoto = QLineEdit()
        self.textboxTotalAPagarSacarMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        self.textboxTotalAPagarSacarMoto.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(self.textboxTotalAPagarSacarMoto, 7, 6, 1, 1, alignment=Qt.AlignTop| Qt.AlignCenter)
        self.textboxTotalAPagarSacarMoto.setReadOnly(True)
        # Crea un boton para facturar
        self.boton_facturar = QPushButton('Facturar')
        self.boton_facturar.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        self.boton_facturar.setDisabled(True)
        # Conectar el botón de imprimir a la función registrarMoto
        self.boton_facturar.clicked.connect(lambda: [
            db_connection.registrarSalidaMoto(
            self.textboxCodigoSacarMoto.text(),
            self.textboxTotalAPagarSacarMoto.text()
        ),
        generarTicketSalidaMoto(self.textboxFIngresoSacarMoto.text(),
                                self.textboxFSalidaSacarMoto.text(),
                                self.textboxHIngresoSacarMoto.text(),
                                self.textboxHSalidaSacarMoto.text(),
                                self.textboxTiempoTotalSacarMoto.text(),
                                self.textboxTotalAPagarSacarMoto.text(),
                                self.textboxPlacaSacarMoto.text(),
                                self.textboxCasilleroSacarMoto.text()),
        db_connection.cambiarEstadoCasillero(self.textboxCasilleroSacarMoto.text(),"OCUPADO"),
        self.textboxCodigoSacarMoto.clear(),
        self.textboxPlacaSacarMoto.clear (),
        self.textboxCasilleroSacarMoto.clear(),
        self.textboxCascosSacarMoto.clear(),
        self.textboxFIngresoSacarMoto.clear(),
        self.textboxHIngresoSacarMoto.clear(),
        self.textboxFSalidaSacarMoto.clear(),
        self.textboxHSalidaSacarMoto.clear(),
        self.textboxPagadoPorSacarMoto.clear(),
        self.textboxTiempoTotalSacarMoto.clear(),
        self.textboxTotalAPagarSacarMoto.clear(),
        self.senalActualizarTablasCasilleros.emit(),
        self.senalActualizarTablaRegistroMotos.emit(),
        self.boton_facturar.setDisabled(True)
    ])
        
        
        layout_ticketsSalidaMotos.addWidget(self.boton_facturar, 8, 6, 2, 2,
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
        titulo_tickets.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_ticketsIngresoFijo.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_ticketsIngresoFijo.addWidget(linea_horizontal1, 0, 0, 1, 7, alignment=Qt.AlignBottom)
    #---Fila 1
        # Crear el label "Codigo" y la textbox
        label_codigo = QLabel('Codigo')
        label_codigo.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsIngresoFijo.addWidget(label_codigo, 1, 2, 1, 1, alignment=Qt.AlignCenter)
        # Text box Codigo
        textbox_codigo = QLineEdit()
        textbox_codigo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_codigo.setFixedWidth(240)
        textbox_codigo.setReadOnly(True)
        layout_ticketsIngresoFijo.addWidget(textbox_codigo, 1, 3, 1, 1, alignment=Qt.AlignCenter)
    #---Fila 2
        # Crear el label "Tipo" y la textbox
        label_tipo = QLabel('Tipo')
        label_tipo.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsIngresoFijo.addWidget(label_tipo, 2, 2, 1, 1, alignment=Qt.AlignCenter)
        # combobox box Tipo
        combobox_Tipo = QComboBox()
        combobox_Tipo.addItems(['Puesto', 'Carretilla', 'Otro'])
        combobox_Tipo.setFixedWidth(240)
        combobox_Tipo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 40px;")
        layout_ticketsIngresoFijo.addWidget(combobox_Tipo, 2, 3, 1, 1, alignment=Qt.AlignCenter)
    #---Fila 3
        # Crear el label "Nota" y la textbox
        label_Nota = QLabel('Nota')
        label_Nota.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsIngresoFijo.addWidget(label_Nota, 3, 2, 1, 1, alignment=Qt.AlignCenter)
        # Text box Codigo
        textbox_Nota = QLineEdit()
        textbox_Nota.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Nota.setFixedWidth(240)
        layout_ticketsIngresoFijo.addWidget(textbox_Nota, 3, 3, 1, 1, alignment=Qt.AlignCenter)
    #---Fila 4
        # Crear el label "Valor" y la textbox
        label_Valor = QLabel('Valor')
        label_Valor.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsIngresoFijo.addWidget(label_Valor, 4, 2, 1, 1, alignment=Qt.AlignCenter)
        # Text box Codigo
        textbox_Valor = QLineEdit()
        textbox_Valor.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Valor.setFixedWidth(240)
        layout_ticketsIngresoFijo.addWidget(textbox_Valor, 4, 3, 1, 1, alignment=Qt.AlignCenter)
    #---Fila 5
        # Boton para imprimir
        boton_Imprimir = QPushButton('Imprimir')
        boton_Imprimir.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        layout_ticketsIngresoFijo.addWidget(boton_Imprimir, 5, 3, 1, 1,
                                alignment=Qt.AlignTop| Qt.AlignLeft)
        # Conectar el botón de imprimir a la función registrarMoto
        boton_Imprimir.clicked.connect(lambda: [
            db_connection.registrarFijo(
            combobox_Tipo.currentText(),
            textbox_Nota.text(),
            textbox_Valor.text(),
        ),
        combobox_Tipo.setCurrentIndex(0),
        textbox_Nota.clear(),
        textbox_Valor.clear()
    ])
        layout_ticketsIngresoFijo.setRowStretch(0, 0)
        layout_ticketsIngresoFijo.setRowStretch(1, 1)
        layout_ticketsIngresoFijo.setRowStretch(2, 1)
        layout_ticketsIngresoFijo.setRowStretch(3, 1)
        layout_ticketsIngresoFijo.setRowStretch(4, 1)
        layout_ticketsIngresoFijo.setRowStretch(5, 1)

        #Se agrega el layout a la pagina
        page_ticketsIngresoFijo.setLayout(layout_ticketsIngresoFijo)
        #Se agrega al stack
        self.stacked_widgetTickets.addWidget(page_ticketsIngresoFijo)

    def pantallaSacarFijo(self):
        # Pagina de ticketes salida moto
        page_ticketsSacarFijo = QWidget()
        #layout de el registro de los tickets
        layout_ticketsSacarFijo = QGridLayout()
        #------------------------Salida de fijos------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_tickets = QLabel('REGISTRAR SALIDA FIJO')
        titulo_tickets.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_ticketsSacarFijo.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_ticketsSacarFijo.addWidget(linea_horizontal1, 0, 0, 1, 7, alignment=Qt.AlignBottom)
    #---Buscar
        # Crear el label "Codigo" y la textbox
        label_codigo = QLabel('Codigo')
        label_codigo.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSacarFijo.addWidget(label_codigo, 1, 1, 1, 2, alignment=Qt.AlignCenter)
        # Text box Codigo
        textbox_codigo = QLineEdit()
        textbox_codigo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_codigo.setFixedWidth(240)
        layout_ticketsSacarFijo.addWidget(textbox_codigo, 1, 2, 1, 2, alignment=Qt.AlignCenter)
        # Boton para buscar
        boton_Buscar = QPushButton('Buscar')
        boton_Buscar.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        layout_ticketsSacarFijo.addWidget(boton_Buscar, 1, 5, 1, 2,
                                alignment=Qt.AlignCenter)
    #---Mostrar
    #---Fila 1
        # Crear el label "Tipo" y la textbox
        label_Tipo = QLabel('Tipo')
        label_Tipo.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSacarFijo.addWidget(label_Tipo, 3, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box tipo
        textbox_Tipo = QLineEdit()
        textbox_Tipo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Tipo.setFixedWidth(240)
        layout_ticketsSacarFijo.addWidget(textbox_Tipo, 4, 1, 1, 1, alignment=Qt.AlignTop)
        textbox_Tipo.setReadOnly(True)
        # Crear el label "Nota" y la textbox
        label_Nota = QLabel('Nota')
        label_Nota.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSacarFijo.addWidget(label_Nota, 3, 3, 1, 2, alignment=Qt.AlignTop)
        # Text box Cascos
        textbox_Nota = QLineEdit()
        textbox_Nota.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Nota.setFixedWidth(240)
        layout_ticketsSacarFijo.addWidget(textbox_Nota, 4, 3, 1, 1, alignment= Qt.AlignTop)
        textbox_Nota.setReadOnly(True)
     #---Fila 2
        # Crear el label "Fecha ingreso" y la textbox
        label_FIngreso = QLabel('Fecha ingreso')
        label_FIngreso.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSacarFijo.addWidget(label_FIngreso, 5, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box casillero
        textbox_FIngreso = QLineEdit()
        textbox_FIngreso.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_FIngreso.setFixedWidth(240)
        layout_ticketsSacarFijo.addWidget(textbox_FIngreso, 6, 1, 1, 1, alignment=Qt.AlignTop)
        textbox_FIngreso.setReadOnly(True)
        # Crear el label "Hora ingreso" y la textbox
        label_HIngreso = QLabel('Hora ingreso')
        label_HIngreso.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSacarFijo.addWidget(label_HIngreso, 5, 3, 1, 2, alignment=Qt.AlignTop)
        # Text box Cascos
        textbox_HIngreso = QLineEdit()
        textbox_HIngreso.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_HIngreso.setFixedWidth(240)
        layout_ticketsSacarFijo.addWidget(textbox_HIngreso, 6, 3, 1, 1, alignment= Qt.AlignTop)
        textbox_HIngreso.setReadOnly(True)
    #---Fila 3
        # Crear el label "Fecha salida" y la textbox
        label_FSalida= QLabel('Fecha salida')
        label_FSalida.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSacarFijo.addWidget(label_FSalida, 7, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box casillero
        textbox_FSalida = QLineEdit()
        textbox_FSalida.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_FSalida.setFixedWidth(240)
        layout_ticketsSacarFijo.addWidget(textbox_FSalida, 8, 1, 1, 1, alignment=Qt.AlignTop)
        textbox_FSalida.setReadOnly(True)
        # Crear el label "Hora salida" y la textbox
        label_HSalida = QLabel('Hora salida')
        label_HSalida.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSacarFijo.addWidget(label_HSalida, 7, 3, 1, 2, alignment=Qt.AlignTop)
        # Text box Cascos
        textbox_HSalida = QLineEdit()
        textbox_HSalida.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_HSalida.setFixedWidth(240)
        layout_ticketsSacarFijo.addWidget(textbox_HSalida, 8, 3, 1, 1, alignment= Qt.AlignTop)
        textbox_HSalida.setReadOnly(True)
    #---Fila 4
        # Crear el label "Tiempo total" y la textbox
        label_TiempoTotal = QLabel('Tiempo total')
        label_TiempoTotal.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSacarFijo.addWidget(label_TiempoTotal, 9, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box tiempo total
        textbox_TiempoTotal = QLineEdit()
        textbox_TiempoTotal.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_TiempoTotal.setFixedWidth(240)
        layout_ticketsSacarFijo.addWidget(textbox_TiempoTotal, 10, 1, 1, 1, alignment= Qt.AlignTop)
        textbox_TiempoTotal.setReadOnly(True)
        # Crear el label "Total a pagar" y la textbox
        label_TotalApagar= QLabel('Total a pagar')
        label_TotalApagar.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSacarFijo.addWidget(label_TotalApagar, 5, 5, 1, 2, alignment=Qt.AlignTop)
        # Text box total a pagar
        textbox_TotalApagar = QLineEdit()
        textbox_TotalApagar.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_TotalApagar.setFixedWidth(240)
        layout_ticketsSacarFijo.addWidget(textbox_TotalApagar, 6, 5, 1, 1, alignment=Qt.AlignTop)
        textbox_TotalApagar.setReadOnly(True)
        # Crea un boton para facturar
        boton_facturar = QPushButton('Facturar')
        boton_facturar.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """)
        layout_ticketsSacarFijo.addWidget(boton_facturar, 7, 5, 1, 2,
                                alignment=Qt.AlignTop| Qt.AlignCenter)
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
        layout_ticketsSacarFijo.setRowStretch(9, 1)
        layout_ticketsSacarFijo.setRowStretch(10, 1)  
        #Se agrega el layout a la pagina
        page_ticketsSacarFijo.setLayout(layout_ticketsSacarFijo)
        #Se agrega al stack
        self.stacked_widgetTickets.addWidget(page_ticketsSacarFijo)

    def pantallaIngresarMensualidad(self):
        # Pagina de ticketes salida moto
        page_ticketsIngresarMensualidad = QWidget()
        #layout de el registro de los tickets
        layout_ticketsIngresarMensualidad = QGridLayout()
        #------------------------Salida de fijos------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_tickets = QLabel('REGISTRAR MENSUALIDAD')
        titulo_tickets.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_ticketsIngresarMensualidad.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_ticketsIngresarMensualidad.addWidget(linea_horizontal1, 0, 0, 1, 7, alignment=Qt.AlignBottom)

        #Placa
        titulo_Placa = QLabel('PLACA')
        titulo_Placa .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsIngresarMensualidad.addWidget(titulo_Placa  , 1, 3, 1, 1, alignment= Qt.AlignBottom |Qt.AlignHCenter)
        
        textbox_Placa = QLineEdit()
        textbox_Placa.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Placa.setFixedWidth(200)
        layout_ticketsIngresarMensualidad.addWidget(textbox_Placa, 1, 4, 1, 1, alignment=Qt.AlignHCenter |Qt.AlignBottom)

        #Nombre
        titulo_Nombre = QLabel('NOMBRE')
        titulo_Nombre .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsIngresarMensualidad.addWidget(titulo_Nombre  , 2, 3, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        textbox_Nombre = QLineEdit()
        textbox_Nombre.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Nombre.setFixedWidth(200)
        layout_ticketsIngresarMensualidad.addWidget(textbox_Nombre, 2, 4, 1, 1, alignment=Qt.AlignHCenter |Qt.AlignCenter)

        #Telefono
        titulo_Telefono = QLabel('TELEFONO')
        titulo_Telefono .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsIngresarMensualidad.addWidget(titulo_Telefono  ,3, 3, 1, 1, alignment= Qt.AlignTop |Qt.AlignHCenter)
        
        textbox_Telefono = QLineEdit()
        textbox_Telefono.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Telefono.setFixedWidth(200)
        layout_ticketsIngresarMensualidad.addWidget(textbox_Telefono, 3, 4, 1, 1, alignment=Qt.AlignHCenter |Qt.AlignTop)

        #Boton Imprimir
        boton_imprimir = QPushButton('IMPRIMIR')
        boton_imprimir.setStyleSheet("color: White; background-color: #222125; font-size: 35px; border-radius: 15px; padding: 10px 20px;")
        layout_ticketsIngresarMensualidad.addWidget(boton_imprimir,3, 0, 2, 7,alignment=Qt.AlignHCenter |Qt.AlignCenter)

        #Mensualidades Vigentes
        titulo_Telefono = QLabel('Mensualidades\nVigentes')
        # Centrar el texto en el QLabel
        titulo_Telefono.setAlignment(Qt.AlignCenter)
        titulo_Telefono .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsIngresarMensualidad.addWidget(titulo_Telefono  ,6, 0, 2, 7, alignment= Qt.AlignCenter |Qt.AlignLeft)
        
        textbox_Telefono = QLineEdit()
        textbox_Telefono.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Telefono.setFixedWidth(60)
        layout_ticketsIngresarMensualidad.addWidget(textbox_Telefono, 6, 3, 2, 1, alignment=Qt.AlignLeft |Qt.AlignCenter)

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
        # Pagina de ticketes salida moto
        page_ticketsRenovarMensualidad = QWidget()
        #layout de el registro de los tickets
        layout_ticketsRenovarMensualidad = QGridLayout()
        #------------------------Salida de fijos------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_tickets = QLabel('RENOVAR MENSUALIDAD')
        titulo_tickets.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_ticketsRenovarMensualidad.addWidget(titulo_tickets, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_ticketsRenovarMensualidad.addWidget(linea_horizontal1, 0, 0, 1, 7, alignment=Qt.AlignBottom)

        #Codigo
        titulo_Codigo = QLabel('CODIGO')
        titulo_Codigo.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsRenovarMensualidad.addWidget(titulo_Codigo  , 1, 2, 1, 1, alignment= Qt.AlignBottom |Qt.AlignHCenter)
        
        textbox_Codigo = QLineEdit()
        textbox_Codigo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Codigo.setFixedWidth(150)
        layout_ticketsRenovarMensualidad.addWidget(textbox_Codigo, 1, 3, 1, 2, alignment=Qt.AlignHCenter |Qt.AlignBottom)
        #Placa
        titulo_Placa = QLabel('PLACA')
        titulo_Placa .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsRenovarMensualidad.addWidget(titulo_Placa  , 2, 2, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        textbox_Placa = QLineEdit()
        textbox_Placa.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Placa.setFixedWidth(150)
        layout_ticketsRenovarMensualidad.addWidget(textbox_Placa, 2, 3, 1, 2, alignment=Qt.AlignHCenter |Qt.AlignCenter)

        #Boton Buscar
        boton_Buscar = QPushButton('BUSCAR')
        boton_Buscar.setStyleSheet("color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;")
        layout_ticketsRenovarMensualidad.addWidget(boton_Buscar,1, 5, 2, 2,alignment=Qt.AlignLeft |Qt.AlignCenter)

        #Nombre
        titulo_Nombre = QLabel('NOMBRE')
        titulo_Nombre.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsRenovarMensualidad.addWidget(titulo_Nombre  , 3, 1, 1, 3, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        textbox_Nombre = QLineEdit()
        textbox_Nombre.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Nombre.setFixedWidth(250)
        layout_ticketsRenovarMensualidad.addWidget(textbox_Nombre, 4, 1, 1, 3, alignment=Qt.AlignTop |Qt.AlignHCenter)

        #Fecha de Ingreso
        titulo_FechaIngreso = QLabel('FECHA INGRESO')
        titulo_FechaIngreso.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsRenovarMensualidad.addWidget(titulo_FechaIngreso  , 5, 1, 1, 3, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        textbox_FechaIngreso = QLineEdit()
        textbox_FechaIngreso.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_FechaIngreso.setFixedWidth(250)
        layout_ticketsRenovarMensualidad.addWidget(textbox_FechaIngreso, 6, 1, 1, 3, alignment=Qt.AlignHCenter |Qt.AlignTop)

        #Dias Trasncurridos
        titulo_DiasTranscurridos = QLabel('DIAS\nTRANSCURRIDOS')
        titulo_DiasTranscurridos.setAlignment(Qt.AlignCenter)
        titulo_DiasTranscurridos.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsRenovarMensualidad.addWidget(titulo_DiasTranscurridos  , 7, 1, 1, 3, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        textbox_DiasTranscurridos = QLineEdit()
        textbox_DiasTranscurridos.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_DiasTranscurridos.setFixedWidth(250)
        layout_ticketsRenovarMensualidad.addWidget(textbox_DiasTranscurridos, 8, 1, 1, 3, alignment=Qt.AlignTop |Qt.AlignHCenter)
              
        #Telefono
        titulo_Telefono = QLabel('TELEFONO')
        titulo_Telefono.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsRenovarMensualidad.addWidget(titulo_Telefono  , 3, 3, 1, 4, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        textbox_Telefono = QLineEdit()
        textbox_Telefono.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Telefono.setFixedWidth(250)
        layout_ticketsRenovarMensualidad.addWidget(textbox_Telefono, 4, 3, 1, 4, alignment=Qt.AlignTop |Qt.AlignHCenter)

        #Hora de Ingreso
        titulo_HoraIngreso = QLabel('HORA INGRESO')
        titulo_HoraIngreso.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_ticketsRenovarMensualidad.addWidget(titulo_HoraIngreso  , 5, 3, 1, 4, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        textbox_HoraIngreso = QLineEdit()
        textbox_HoraIngreso.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_HoraIngreso.setFixedWidth(250)
        layout_ticketsRenovarMensualidad.addWidget(textbox_HoraIngreso, 6, 3, 1, 4, alignment=Qt.AlignHCenter |Qt.AlignTop)

        #Boton Renovar
        boton_renovar = QPushButton('RENOVAR')
        boton_renovar.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 20px;")
        layout_ticketsRenovarMensualidad.addWidget(boton_renovar,7, 3, 2, 4,alignment=Qt.AlignHCenter |Qt.AlignCenter)

        # Establecer las proporciones de las filas en la cuadricula
        layout_ticketsRenovarMensualidad.setRowStretch(0, 0)
        layout_ticketsRenovarMensualidad.setRowStretch(1, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(2, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(3, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(5, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(6, 1)
        layout_ticketsRenovarMensualidad.setRowStretch(7, 1)  
        layout_ticketsRenovarMensualidad.setRowStretch(8, 1)
        #Se agrega el layout a la pagina
        page_ticketsRenovarMensualidad.setLayout(layout_ticketsRenovarMensualidad)
        #Se agrega al stack
        self.stacked_widgetTickets.addWidget(page_ticketsRenovarMensualidad)