import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
#Configuración de la pantalla
    def initUI(self):
        self.setWindowTitle('SOFTWARE PARQUEADERO')
        self.setStyleSheet("background-color: #151419;")
        self.setWindowState(Qt.WindowMaximized)
        self.stacked_widget = QStackedWidget(self)  # Mover la creación aquí
        #self.setMinimumSize(1300, 720)
        self.Pagina_principal()
        self.pagina_registros()
        self.pagina_Tickets()
        self.pagina_Casilleros()
        self.pagina_Reportes()
    #Panel principal (Menú vertical izquierdo)
    def Pagina_principal(self):
        main_layout = QHBoxLayout(self)

        # Creando el menú de la izquierda
        menuizquierdo = QWidget()
        layout_menu = QVBoxLayout(menuizquierdo)

        self.menu_label = QLabel('MENÚ', self)
        self.menu_label.setStyleSheet("color: #888888; font-size: 20px; font-weight: bold;")
        layout_menu.addWidget(self.menu_label, alignment=Qt.AlignCenter)

        self.line_frame2 = QFrame(self)
        self.line_frame2.setFrameShape(QFrame.HLine)
        self.line_frame2.setLineWidth(2)
        self.line_frame2.setStyleSheet("color: #222126;")
        layout_menu.addWidget(self.line_frame2, alignment=Qt.AlignTop)

        self.botonRegistros = QPushButton('Registro de ingresos', self)
        self.botonRegistros.setStyleSheet("background-color: #222125; color: White; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        self.botonRegistros.setIcon(QIcon('registrosSel.png'))
        self.botonRegistros.setCheckable(True)
        self.botonRegistros.setChecked(True)
        self.botonRegistros.pressed.connect(self.cambiar_color)
        self.botonRegistros.clicked.connect(self.pagina_registros)
        layout_menu.addWidget(self.botonRegistros, alignment=Qt.AlignCenter)

        self.botontickets = QPushButton('Generar Tickets', self)
        self.botontickets.setStyleSheet("background-color: #151419; color: #737074; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        self.botontickets.setIcon(QIcon('ticketMotos.png'))
        self.botontickets.setCheckable(True)
        self.botontickets.pressed.connect(self.cambiar_color)
        self.botontickets.clicked.connect(self.pagina_Tickets)
        layout_menu.addWidget(self.botontickets, alignment=Qt.AlignCenter)

        self.botonGestionarCasilleros = QPushButton('Gestionar casilleros', self)
        self.botonGestionarCasilleros.setStyleSheet("background-color: #151419; color: #737074; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        self.botonGestionarCasilleros.setIcon(QIcon('gestionCasilleros.png'))
        self.botonGestionarCasilleros.setCheckable(True)
        self.botonGestionarCasilleros.pressed.connect(self.cambiar_color)
        self.botonGestionarCasilleros.clicked.connect(self.pagina_Casilleros)
        layout_menu.addWidget(self.botonGestionarCasilleros, alignment=Qt.AlignCenter)

        self.botonReportes = QPushButton('Gestión de reportes', self)
        self.botonReportes.setStyleSheet("background-color: #151419; color: #737074; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        self.botonReportes.setIcon(QIcon('reportes.png'))
        self.botonReportes.setCheckable(True)
        self.botonReportes.pressed.connect(self.cambiar_color)
        self.botonReportes.clicked.connect(self.pagina_Reportes)
        layout_menu.addWidget(self.botonReportes, alignment=Qt.AlignCenter)
        layout_menu.setAlignment(Qt.AlignTop)
        self.stacked_widget = QStackedWidget(self)
        main_layout.addWidget(menuizquierdo)
        main_layout.addWidget(self.stacked_widget)

        self.ultimo_boton_seleccionado = self.botonRegistros
        self.setLayout(main_layout)


    #Tabla de registros
    def pagina_registros(self):
        # Crear el widget de la página de registros
        page_registros = QWidget()

        # Crear un layout para organizar los elementos en la página
        layout_registros = QVBoxLayout(page_registros)

        # Crear el título "Registros"
        titulo_registros = QLabel('REGISTROS INGRESADOS', page_registros)
        titulo_registros.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_registros.addWidget(titulo_registros, alignment=Qt.AlignCenter)
        
        # Crear la tabla de registros
        tabla_registros = QTableWidget(page_registros)
        tabla_registros.setColumnCount(9)  # Definir el número de columnas
        tabla_registros.setHorizontalHeaderLabels(
            ['ID', 'PLACA', 'CASILLERO', 'CASCOS', 'H.INGRESO', 'F.INGRESO', 'H.SALIDA', 'F.SALIDA',
             'TOTAL'])
        tabla_registros.setStyleSheet("""
                    QTableWidget {
                        background-color: #222126;
                        color: white;
                        border: 1px solid #222126;
                        alternate-background-color: #131216; /* Color de fila alternativa */
                    }

                    QTableWidget::item {
                        background-color: #151419; /* Color de fondo de las celdas */
                        border-color: #222126; /* Color del borde de las celdas */
                    }

                    QHeaderView::section {
                        background-color: #151419; /* Color de fondo de las cabeceras de las columnas */
                        color: white; /* Color del texto de las cabeceras de las columnas */
                        border: none; /* Sin borde */
                        padding: 4px; /* Ajuste del relleno */
                    }

                    QHeaderView::section:hover {
                        background-color: #151419; /* Color de fondo al pasar el mouse */
                    }

                    QHeaderView::section:selected {
                        background-color: #151419; /* Color de fondo al seleccionar */
                    }
                """)
        # Calcular el ancho de cada columna
        ancho_total = 1000  # Ancho total de la tabla
        num_columnas = 9
        ancho_columna = ancho_total / num_columnas

        # Establecer el ancho de cada columna
        for i in range(num_columnas):
            tabla_registros.setColumnWidth(i, int(ancho_columna))

        # Añadir la tabla a la disposición
        layout_registros.addWidget(tabla_registros)

        # Crear un layout horizontal para los elementos debajo de la tabla
        layout_botones = QHBoxLayout()

        # Crear combo box, text box y boton para la parte izquierda
        combo_box = QComboBox()
        text_box = QLineEdit()
        boton_izquierda = QPushButton('Buscar')

        # Establecer el estilo del QPushButton
        boton_izquierda.setStyleSheet("background-color: #222125; color: white;")

        layout_botones.addWidget(combo_box)
        combo_box.addItems(['Placa', 'ID', 'Casillero'])
        combo_box.setStyleSheet("color: white; border: 1px solid white;")
        layout_botones.addWidget(text_box)
        text_box.setStyleSheet("color: white; border: 1px solid white;")
        layout_botones.addWidget(boton_izquierda)
        layout_botones.addStretch()  # Agregar espacio elástico para separar los elementos izquierdos de los derechos

        # Crear botones para la parte derecha
        boton_mensualidades = QPushButton('Lista mensualidades', page_registros)
        boton_guardar = QPushButton('Guardar edicion', page_registros)
        boton_limpiar = QPushButton('Limpiar registros', page_registros)

        # Establecer el estilo de los botones
        boton_mensualidades.setStyleSheet("background-color: #222125; color: white;")
        boton_guardar.setStyleSheet("background-color: #222125; color: white;")
        boton_limpiar.setStyleSheet("background-color: #222125; color: white;")

        layout_botones.addWidget(boton_mensualidades)
        layout_botones.addWidget(boton_guardar)
        layout_botones.addWidget(boton_limpiar)

        # Agregar el layout horizontal a la disposición principal
        layout_registros.addLayout(layout_botones)

        # Establecer el layout principal para la página
        page_registros.setLayout(layout_registros)

        # Agregar la página al QStackedWidget
        self.stacked_widget.addWidget(page_registros)

    #Registrar ingresos y generar ticket
    def pagina_Tickets(self):
        # Crear el widget de la página de Tickets
        page_tickets = QWidget()

        # Crear un layout de cuadrícula para organizar la página en dos secciones
        layout_tickets = QGridLayout(page_tickets)

        # Crear el título "Generar Tickets" y añadirlo a la sección izquierda
        titulo_tickets = QLabel('Generar Tickets', page_tickets)
        titulo_tickets.setStyleSheet("color: #888888;font-size: 60px; font-weight: bold;")
        layout_tickets.addWidget(titulo_tickets, 0, 0, 1, 7,
                                 alignment=Qt.AlignTop | Qt.AlignCenter)  # Span 1 fila y 3 columnas
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame(page_tickets)
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_tickets.addWidget(linea_horizontal1, 0, 0, 1, 7,
                                  alignment=Qt.AlignBottom)

        # Crear el label "Placa" y la textbox
        label_placa = QLabel('Placa:', page_tickets)
        label_placa.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_tickets.addWidget(label_placa, 1, 2, 1, 1,
                                 alignment=Qt.AlignCenter| Qt.AlignRight)  # Alineamiento arriba y a la izquierda
        textbox_placa = QLineEdit(page_tickets)
        textbox_placa.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_placa.setFixedWidth(240)  # Establecer el ancho fijo
        layout_tickets.addWidget(textbox_placa, 1, 3, 1, 1,
                                 alignment=Qt.AlignCenter | Qt.AlignLeft)  # Alineamiento arriba y a la izquierda

        # Crear el label "Cascos" y el combobox
        label_cascos = QLabel('Cascos:', page_tickets)
        label_cascos.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_tickets.addWidget(label_cascos, 2, 2, 1, 1,
                                 alignment=Qt.AlignCenter| Qt.AlignRight)  # Alineamiento arriba y a la izquierda
        combobox_cascos = QComboBox(page_tickets)
        combobox_cascos.addItems(['0', '1', '2'])
        combobox_cascos.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 40px;")
        combobox_cascos.setFixedWidth(60)  # Establecer el ancho fijo
        layout_tickets.addWidget(combobox_cascos, 2, 3, 1, 1,
                                 alignment=Qt.AlignCenter | Qt.AlignLeft)  # Alineamiento arriba y a la izquierda

        # Crear el label "Tiempo" y el combobox
        label_Tiempo = QLabel('Tiempo:', page_tickets)
        label_Tiempo.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_tickets.addWidget(label_Tiempo, 3, 2, 1, 1,
                                 alignment=Qt.AlignCenter | Qt.AlignRight)  # Alineamiento arriba y a la izquierda
        combobox_Tiempo = QComboBox(page_tickets)
        combobox_Tiempo.addItems(['Hora', 'Dia', 'Mes'])
        combobox_Tiempo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 40px;")
        combobox_Tiempo.setFixedWidth(120)  # Establecer el ancho fijo
        layout_tickets.addWidget(combobox_Tiempo, 3, 3, 1, 1,
                                 alignment=Qt.AlignCenter | Qt.AlignLeft)  # Alineamiento arriba y a la izquierda
        # Crea una checkbox para confirmar que se eligio dia o mes  en "combobox_Tiempo"
        checkbox_opcion = QCheckBox('Confirmar', page_tickets)
        checkbox_opcion.setStyleSheet("color: #FFFFFF; font-size: 20px;")
        checkbox_opcion.setChecked(False)  # Opcional: Puedes establecer si la casilla está marcada por defecto o no
        layout_tickets.addWidget(checkbox_opcion, 3, 3, 1, 1,
                                 alignment= Qt.AlignCenter |Qt.AlignRight)
        # Crear el label "Casillero" y el combobox
        label_casillero = QLabel('Casillero:', page_tickets)
        label_casillero.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_tickets.addWidget(label_casillero, 4, 2, 1, 1,
                                 alignment=Qt.AlignCenter | Qt.AlignRight)  # Alineamiento arriba y a la izquierda
        textbox_casillero = QLineEdit(page_tickets)
        textbox_casillero.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_casillero.setReadOnly(True)
        textbox_casillero.setFixedWidth(100)  # Establecer el ancho fijo
        textbox_casillero.setFixedHeight(50)
        layout_tickets.addWidget(textbox_casillero, 4, 3, 1, 1,
                                 alignment=Qt.AlignCenter | Qt.AlignLeft)  # Alineamiento arriba y a la izquierda
        
        # Crea un boton para cambiar al siguiente casillero disponible
        boton_cambiarcasillero = QPushButton('Siguiente', page_tickets)
        boton_cambiarcasillero.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_tickets.addWidget(boton_cambiarcasillero, 4, 3, 1, 1,
                                 alignment=Qt.AlignCenter | Qt.AlignRight)

        # Crear el label "Casilleros disponibles" y el combobox
        label_casillerosDis = QLabel('Casilleros disponibles:', page_tickets)
        label_casillerosDis.setStyleSheet("color: #FFFFFF;font-size: 30px;")
        layout_tickets.addWidget(label_casillerosDis, 5, 2, 1, 1,
                                 alignment=Qt.AlignCenter | Qt.AlignRight)  # Alineamiento arriba y a la izquierda
        #Crear Textbox "Casilleros disponibles" 
        textbox_casillerosDis = QLineEdit(page_tickets)
        textbox_casillerosDis.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 10px;")
        textbox_casillerosDis.setReadOnly(True)
        textbox_casillerosDis.setFixedWidth(70)  # Establecer el ancho fijo
        textbox_casillerosDis.setFixedHeight(50)
        layout_tickets.addWidget(textbox_casillerosDis, 5, 3, 1, 1,
                                 alignment=Qt.AlignCenter | Qt.AlignLeft)  # Alineamiento arriba y a la izquierda
        # Crea un boton para Imprimir
        boton_imprimir = QPushButton('Imprimir', page_tickets)
        boton_imprimir.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
        layout_tickets.addWidget(boton_imprimir, 6, 3, 1, 1,
                                 alignment=Qt.AlignTop | Qt.AlignLeft)
        
        # Establecer las proporciones de las filas en la cuadricula
        layout_tickets.setRowStretch(0, 1)
        layout_tickets.setRowStretch(1, 1)
        layout_tickets.setRowStretch(2, 1)
        layout_tickets.setRowStretch(3, 1)
        layout_tickets.setRowStretch(4, 1)
        layout_tickets.setRowStretch(5, 1)
        layout_tickets.setRowStretch(6, 1)
        #---- Menu lateral
        page_registrosMenu = QWidget()
        layout_ticketsmenu = QGridLayout(page_registrosMenu)

        # Crear la línea vertical de 1 pixel y añadirla a la cuadrícula
        linea_vertical = QFrame(page_tickets)
        linea_vertical.setFrameShape(QFrame.VLine)
        linea_vertical.setLineWidth(1)
        linea_vertical.setStyleSheet("color: #FFFFFF;")
        layout_ticketsmenu.addWidget(linea_vertical, 0, 0, 8, 1)
        # Crear la sección derecha con el título "Menú"
        titulo_menu = QLabel('Menú', page_tickets)
        titulo_menu.setStyleSheet("color: #888888;font-size: 60px; font-weight: bold;")
        layout_ticketsmenu.addWidget(titulo_menu, 0, 1, 1, 2,
                                 alignment=Qt.AlignTop | Qt.AlignCenter)  # Span 1 fila y 1 columna
        linea_horizontal2 = QFrame(page_tickets)
        linea_horizontal2.setFrameShape(QFrame.HLine)
        linea_horizontal2.setLineWidth(1)
        linea_horizontal2.setStyleSheet("color: #FFFFFF;")
        layout_ticketsmenu.addWidget(linea_horizontal2, 0, 1, 1, 2,
                                 alignment=Qt.AlignBottom)
        layout_ticketsmenu.setRowStretch(0, 1)
        layout_ticketsmenu.setRowStretch(1, 1)
        layout_ticketsmenu.setRowStretch(2, 1)
        layout_ticketsmenu.setRowStretch(3, 1)
        layout_ticketsmenu.setRowStretch(4, 1)
        layout_ticketsmenu.setRowStretch(5, 1)
        layout_ticketsmenu.setRowStretch(6, 1)
        # Crea un boton para ingresar a generar ticket ingresar moto
        boton_IngresarM = QPushButton('', page_tickets)
        boton_IngresarM.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_IngresarM.setIcon(QIcon('IngresoMoto.png'))  # Establecer el icono
        boton_IngresarM.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarM, 1, 1, 1, 1,
                                 alignment=Qt.AlignTop | Qt.AlignRight| Qt.AlignCenter)

        # Crea un boton para ingresar a generar ticket sacar moto
        boton_SacarM = QPushButton('', page_tickets)
        boton_SacarM.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_SacarM.setIcon(QIcon('SalidaMoto.png'))  # Establecer el icono
        boton_SacarM.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarM, 1, 2, 1, 1,
                                 alignment=Qt.AlignTop | Qt.AlignLeft| Qt.AlignCenter)
        # Crea un boton para ingresar a generar ticket ingresar Fijo
        boton_IngresarF = QPushButton('', page_tickets)
        boton_IngresarF.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_IngresarF.setIcon(QIcon('IngresoFijo.png'))  # Establecer el icono
        boton_IngresarF.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_IngresarF, 2, 1, 5, 1,
                                 alignment=Qt.AlignTop | Qt.AlignRight| Qt.AlignCenter)
        # Crea un boton para ingresar a generar ticket sacar Fijo
        boton_SacarF = QPushButton('', page_tickets)
        boton_SacarF.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 10px;")
        boton_SacarF.setIcon(QIcon('SalidaFijo.png'))  # Establecer el icono
        boton_SacarF.setIconSize(QSize(100, 100))  # Establecer el tamaño del icono
        layout_ticketsmenu.addWidget(boton_SacarF , 2, 2, 5, 1,
                                 alignment=Qt.AlignTop | Qt.AlignLeft| Qt.AlignCenter)
        page_registrosMenu.setLayout(layout_ticketsmenu)
        layout_tickets.addWidget(page_registrosMenu,0,8,8,2)

        # Establecer el alineamiento vertical de la cuadrícula
        layout_tickets.setAlignment(Qt.AlignTop)

        # Agregar el layout de la cuadrícula a la página
        page_tickets.setLayout(layout_tickets)

        # Agregar la página al QStackedWidget
        self.stacked_widget.addWidget(page_tickets)

    #Configuración de casilleros
    def pagina_Casilleros(self):
        # Crear el widget de la página de registros
        page_casilleros = QWidget()

        # Crear un layout para organizar los elementos en la página
        layout_tickets = QVBoxLayout(page_casilleros)

        # Crear el título "Registros"
        titulo_tickets = QLabel('Gestionar Casilleros', page_casilleros)
        titulo_tickets.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_tickets.addWidget(titulo_tickets, alignment=Qt.AlignCenter)
        self.stacked_widget.addWidget(page_casilleros)

    #Menú para generar reportes
    def pagina_Reportes(self):
        # Crear el widget de la página de registros
        page_reportes = QWidget()

        # Crear un layout para organizar los elementos en la página
        layout_reportes = QVBoxLayout(page_reportes)

        # Crear el título "Registros"
        titulo_tickets = QLabel('Gestionar Reportes', page_reportes)
        titulo_tickets.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_reportes.addWidget(titulo_tickets, alignment=Qt.AlignCenter)
        self.stacked_widget.addWidget(page_reportes)

    #Cambiar color de los botones
    def cambiar_color(self):
        sender = self.sender()
        sender.setStyleSheet("background-color: #222125; color: white; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        boton_actual = self.sender()

        if boton_actual != self.ultimo_boton_seleccionado:
            if self.ultimo_boton_seleccionado:
                self.ultimo_boton_seleccionado.setChecked(False)
                self.ultimo_boton_seleccionado.setStyleSheet("background-color: #151419; color: #737074; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
            self.ultimo_boton_seleccionado = boton_actual
        if sender.text() == "Registro de ingresos":
            self.stacked_widget.setCurrentIndex(0)
        elif sender.text() == "Generar Tickets":
            self.stacked_widget.setCurrentIndex(1)
        elif sender.text() == "Gestionar casilleros":
            self.stacked_widget.setCurrentIndex(2)
        elif sender.text() == "Gestión de reportes":
            self.stacked_widget.setCurrentIndex(3)

#Iniciar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())

