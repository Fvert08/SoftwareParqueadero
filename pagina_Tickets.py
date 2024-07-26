from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
from DatabaseConnection import DatabaseConnection
from config import DB_CONFIG
from PyQt5.QtCore import pyqtSignal
class PaginaTickets(QWidget):
    senalActualizarTablasCasilleros= pyqtSignal()
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()
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
        boton_IngresarM.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_IngresarM.setIcon(QIcon('IngresoMoto.png'))  # Establecer el icono
        boton_IngresarM.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarM, 1, 1, 1, 1, alignment=Qt.AlignTop | Qt.AlignRight | Qt.AlignCenter)
        boton_IngresarM.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(0))


        # Crea un boton para ingresar a generar ticket sacar moto
        boton_SacarM = QPushButton()
        boton_SacarM.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_SacarM.setIcon(QIcon('SalidaMoto.png'))  # Establecer el icono
        boton_SacarM.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarM, 1, 2, 1, 1, alignment=Qt.AlignTop | Qt.AlignLeft | Qt.AlignCenter)
        boton_SacarM.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(1))


        # Crea un boton para ingresar a generar ticket ingresar Fijo
        boton_IngresarF = QPushButton()
        boton_IngresarF.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_IngresarF.setIcon(QIcon('IngresoFijo.png'))  # Establecer el icono
        boton_IngresarF.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarF, 2, 1, 5, 1, alignment=Qt.AlignTop | Qt.AlignRight | Qt.AlignCenter)
        boton_IngresarF.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(2))

        # Crea un boton para ingresar a generar ticket sacar Fijo
        boton_SacarF = QPushButton()
        boton_SacarF.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_SacarF.setIcon(QIcon('SalidaFijo.png'))  # Establecer el icono
        boton_SacarF.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarF, 2, 2, 5, 1, alignment=Qt.AlignTop | Qt.AlignLeft | Qt.AlignCenter)
        boton_SacarF.clicked.connect(lambda: self.stacked_widgetTickets.setCurrentIndex(3))
        
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
        boton_cambiarcasillero.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
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
        boton_imprimir.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
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
        self.senalActualizarTablasCasilleros.emit()
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
        textbox_codigo = QLineEdit()
        textbox_codigo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_codigo.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_codigo, 1, 3, 1, 1, alignment=Qt.AlignCenter | Qt.AlignLeft)
        #-----
        # Crear el label "Placa" y la textbox
        label_placa = QLabel('Placa:')
        label_placa.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_ticketsSalidaMotos.addWidget(label_placa, 2, 2, 1, 1, alignment=Qt.AlignTop | Qt.AlignRight)
        # Text box codigo
        textbox_Placa = QLineEdit()
        textbox_Placa.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_Placa.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_Placa, 2, 3, 1, 1, alignment=Qt.AlignTop| Qt.AlignLeft)
        #----
        # Crea un boton para buscar
        boton_buscar = QPushButton('Buscar')
        boton_buscar.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
        layout_ticketsSalidaMotos.addWidget(boton_buscar, 1, 6, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignLeft)
#----Mostrar---
    #---Fila 1
        # Crear el label "Casillero" y la textbox
        label_casillero = QLabel('Casillero')
        label_casillero.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_casillero, 3, 1, 1, 1, alignment=Qt.AlignTop)
        # Text box casillero
        textbox_casillero = QLineEdit()
        textbox_casillero.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        textbox_casillero.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_casillero, 4, 1, 1, 1, alignment=Qt.AlignTop)
        textbox_casillero.setReadOnly(True)
        # Crear el label "Cascos" y la textbox
        label_cascos = QLabel('Cascos')
        label_cascos.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_cascos, 3, 3, 1, 1, alignment=Qt.AlignTop)
        # Text box Cascos
        textbox_cascos = QLineEdit()
        textbox_cascos.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        textbox_cascos.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_cascos, 4, 3, 1, 1, alignment= Qt.AlignTop)
        textbox_cascos.setReadOnly(True)
     #---Fila 2
        # Crear el label "Fecha ingreso" y la textbox
        label_FIngreso = QLabel('Fecha ingreso')
        label_FIngreso.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_FIngreso, 5, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box casillero
        textbox_FIngreso = QLineEdit()
        textbox_FIngreso.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        textbox_FIngreso.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_FIngreso, 6, 1, 1, 1, alignment=Qt.AlignTop)
        textbox_FIngreso.setReadOnly(True)
        # Crear el label "Hora ingreso" y la textbox
        label_HIngreso = QLabel('Hora ingreso')
        label_HIngreso.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_HIngreso, 5, 3, 1, 2, alignment=Qt.AlignTop)
        # Text box Cascos
        textbox_HIngreso = QLineEdit()
        textbox_HIngreso.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        textbox_HIngreso.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_HIngreso, 6, 3, 1, 1, alignment= Qt.AlignTop)
        textbox_HIngreso.setReadOnly(True)
    #---Fila 3
        # Crear el label "Fecha salida" y la textbox
        label_FSalida= QLabel('Fecha salida')
        label_FSalida.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_FSalida, 7, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box casillero
        textbox_FSalida = QLineEdit()
        textbox_FSalida.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        textbox_FSalida.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_FSalida, 8, 1, 1, 1, alignment=Qt.AlignTop)
        textbox_FSalida.setReadOnly(True)
        # Crear el label "Hora salida" y la textbox
        label_HSalida = QLabel('Hora salida')
        label_HSalida.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_HSalida, 7, 3, 1, 2, alignment=Qt.AlignTop)
        # Text box Cascos
        textbox_HSalida = QLineEdit()
        textbox_HSalida.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        textbox_HSalida.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_HSalida, 8, 3, 1, 1, alignment= Qt.AlignTop)
        textbox_HSalida.setReadOnly(True)
    #---Fila 4
        # Crear el label "Pagado por" y la textbox
        label_PagadoPor= QLabel('Pagado por')
        label_PagadoPor.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_PagadoPor, 9, 1, 1, 2, alignment=Qt.AlignTop)
        # Text box casillero
        textbox_PagadoPor = QLineEdit()
        textbox_PagadoPor.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        textbox_PagadoPor.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_PagadoPor, 10, 1, 1, 1, alignment=Qt.AlignTop)
        textbox_PagadoPor.setReadOnly(True)
        # Crear el label "Tiempo total" y la textbox
        label_TiempoTotal = QLabel('Tiempo total')
        label_TiempoTotal.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_TiempoTotal, 9, 3, 1, 2, alignment=Qt.AlignTop)
        # Text box tiempo total
        textbox_TiempoTotal = QLineEdit()
        textbox_TiempoTotal.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        textbox_TiempoTotal.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_TiempoTotal, 10, 3, 1, 1, alignment= Qt.AlignTop)
        textbox_TiempoTotal.setReadOnly(True)
#----Facturar
        # Crear el label "Total a pagar" y la textbox
        label_TotalAPagar = QLabel('Total a pagar')
        label_TotalAPagar.setStyleSheet("color: #FFFFFF;font-size: 37px;")
        layout_ticketsSalidaMotos.addWidget(label_TotalAPagar, 6, 6, 1, 2, alignment=Qt.AlignTop| Qt.AlignCenter)
        # Text box Cascos
        textbox_TotalAPagar = QLineEdit()
        textbox_TotalAPagar.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 27px;")
        textbox_TotalAPagar.setFixedWidth(200)
        layout_ticketsSalidaMotos.addWidget(textbox_TotalAPagar, 7, 6, 1, 1, alignment=Qt.AlignTop| Qt.AlignCenter)
        textbox_TotalAPagar.setReadOnly(True)
        # Crea un boton para facturar
        boton_facturar = QPushButton('Facturar')
        boton_facturar.setStyleSheet(
            "color: White; background-color: #222125; font-size: 27px; border-radius: 15px; padding: 15px 30px;")
        layout_ticketsSalidaMotos.addWidget(boton_facturar, 8, 6, 2, 2,
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
        boton_Imprimir.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
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
        boton_Buscar.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
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
        boton_facturar.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
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

