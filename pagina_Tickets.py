from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
class PaginaTickets(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

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

        # Crea un boton para ingresar a generar ticket sacar Fijo
        boton_SacarF = QPushButton()
        boton_SacarF.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_SacarF.setIcon(QIcon('SalidaFijo.png'))  # Establecer el icono
        boton_SacarF.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarF, 2, 2, 5, 1, alignment=Qt.AlignTop | Qt.AlignLeft | Qt.AlignCenter)
        
        #Se agrega el layout del menú a la página del menú
        page_registrosMenu.setLayout(layout_ticketsmenu)
        #Se agrega el stack al layout principal
        main_layoutRegistros.addWidget(self.stacked_widgetTickets)
        #se agrega el menú al layout principal
        main_layoutRegistros.addWidget(page_registrosMenu)
        #se agrega el layout principal a la pagina principal
        page_principalTickets.setLayout(main_layoutRegistros)
        #Se llama la pantalla para cargarla en el stack
        self.pantallaIngresoMotos()
        #se llama la primera posición del stack
        self.stacked_widgetTickets.setCurrentIndex(0)
        #se agrega toda la pagina al stack principal de la app
        self.stacked_widget.addWidget(page_principalTickets)
    def pantallaIngresoMotos (self):
        # Pagina de ticketes ingreso
        page_tickets = QWidget()
        page_prueba = QWidget()
        #layout de el registro de los tickets
        layout_ticketsIngresoMotos = QGridLayout()
        #------------------------Ingreso de motos------------------------------------
        # Crear el título "Generar Tickets" y añadirlo a la sección izquierda
        titulo_tickets = QLabel('Generar Tickets')
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
        combobox_Tiempo.addItems(['Hora', 'Dia', 'Mes'])
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
        textbox_casillero = QLineEdit(page_tickets)
        textbox_casillero.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_casillero.setReadOnly(True)
        textbox_casillero.setFixedWidth(100)  # Establecer el ancho fijo
        textbox_casillero.setFixedHeight(50)
        layout_ticketsIngresoMotos.addWidget(textbox_casillero, 4, 3, 1, 1,
                                alignment=Qt.AlignCenter | Qt.AlignLeft)  # Alineamiento arriba y a la izquierda
        
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
        textbox_casillerosDis = QLineEdit(page_tickets)
        textbox_casillerosDis.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 10px;")
        textbox_casillerosDis.setReadOnly(True)
        textbox_casillerosDis.setFixedWidth(70)  # Establecer el ancho fijo
        textbox_casillerosDis.setFixedHeight(50)
        layout_ticketsIngresoMotos.addWidget(textbox_casillerosDis, 5, 3, 1, 1,
                                alignment=Qt.AlignCenter | Qt.AlignLeft)  # Alineamiento arriba y a la izquierda
        # Crea un boton para Imprimir
        boton_imprimir = QPushButton('Imprimir', page_tickets)
        boton_imprimir.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
        layout_ticketsIngresoMotos.addWidget(boton_imprimir, 6, 3, 1, 1,
                                alignment=Qt.AlignTop | Qt.AlignLeft)
        
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
        self.stacked_widgetTickets.addWidget(page_prueba)
        