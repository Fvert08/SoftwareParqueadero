from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout,QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
class PaginaCasilleros(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        # Crear el widget de la página de registros
        page_casilleros = QWidget()

        # Crear un layout para organizar los elementos en la página
        layout_tickets = QGridLayout()

        titulo_casilleros = QLabel('GESTIONAR CASILLEROS')
        titulo_casilleros.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_tickets.addWidget(titulo_casilleros, 0, 0, 1, 10, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_tickets.addWidget(linea_horizontal1, 0, 0, 1, 10, alignment=Qt.AlignBottom)

        titulo_tablacasilleros = QLabel('CASILLEROS')
        titulo_tablacasilleros.setStyleSheet("color: #FFFFFF;font-size: 40px; font-weight: bold;")
        layout_tickets.addWidget(titulo_tablacasilleros, 1, 0, 1, 4, alignment= Qt.AlignCenter |Qt.AlignTop)
        
        titulo_agregarCasillero = QLabel('AGREGAR CASILLERO')
        titulo_agregarCasillero.setStyleSheet("color: #FFFFFF;font-size: 20px; font-weight: bold;")
        layout_tickets.addWidget(titulo_agregarCasillero, 7, 0, 1, 4, alignment= Qt.AlignCenter |Qt.AlignTop)

        titulo_numero = QLabel('NUMERO')
        titulo_numero .setStyleSheet("color: #FFFFFF;font-size: 20px; font-weight: bold;")
        layout_tickets.addWidget(titulo_numero , 7, 0, 1, 1, alignment= Qt.AlignCenter |Qt.AlignBottom)

        textbox_numero = QLineEdit()
        textbox_numero.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_numero.setFixedWidth(130)
        layout_tickets.addWidget(textbox_numero, 7, 1, 1, 1, alignment=Qt.AlignCenter |Qt.AlignBottom)

        titulo_pc = QLabel('PC')
        titulo_pc.setStyleSheet("color: #FFFFFF;font-size: 20px; font-weight: bold;")
        layout_tickets.addWidget(titulo_pc , 7, 2, 1, 1, alignment= Qt.AlignLeft |Qt.AlignBottom)

        combobox_pc = QComboBox()
        combobox_pc.addItems(['1', '2'])
        combobox_pc.setFixedWidth(50)
        combobox_pc.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 20px;")
        layout_tickets.addWidget(combobox_pc,7, 2, 1, 1, alignment=Qt.AlignRight |Qt.AlignBottom)

        titulo_estado = QLabel('ESTADO')
        titulo_estado .setStyleSheet("color: #FFFFFF;font-size: 20px; font-weight: bold;")
        layout_tickets.addWidget(titulo_estado , 8, 0, 1, 1, alignment= Qt.AlignCenter )

        combobox_Estado = QComboBox()
        combobox_Estado.addItems(['OCUPADO', 'DISPONIBLE'])
        combobox_Estado.setFixedWidth(130)
        combobox_Estado.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 20px;")
        layout_tickets.addWidget(combobox_Estado,8, 1, 1, 1, alignment=Qt.AlignCenter )

        boton_agregar = QPushButton('AGREGAR')
        boton_agregar.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_tickets.addWidget(boton_agregar,8, 2, 1, 2, alignment=Qt.AlignLeft)
        
        
        tabla_registros = QTableWidget(self)
        tabla_registros.setColumnCount(4)  # Definir el número de columnas
        tabla_registros.setHorizontalHeaderLabels(
            ['NUMERO', 'ESTADO', 'PLACA', 'PC'])
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
        header = tabla_registros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        layout_tickets.addWidget(tabla_registros, 2, 0, 5, 4)

        boton_desocupar = QPushButton('DESOCUPAR')
        boton_desocupar.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_tickets.addWidget(boton_desocupar, 2, 4, 2, 2,
                                alignment=Qt.AlignTop| Qt.AlignHCenter)
        
        boton_bloquear = QPushButton('BLOQUEAR')
        boton_bloquear.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_tickets.addWidget(boton_bloquear, 2, 4, 2, 2,
                                alignment=Qt.AlignCenter| Qt.AlignHCenter)
        
        boton_eliminar = QPushButton('ELIMINAR')
        boton_eliminar.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_tickets.addWidget(boton_eliminar, 2, 4, 2, 2,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        
        titulo_cambiarPc = QLabel('CAMBIAR PC')
        titulo_cambiarPc .setStyleSheet("color: #FFFFFF;font-size: 20px; font-weight: bold;")
        layout_tickets.addWidget(titulo_cambiarPc, 4, 4, 1, 2,
                                alignment=Qt.AlignCenter| Qt.AlignHCenter)
        
        titulo_pcCambiar = QLabel('PC')
        titulo_pcCambiar.setStyleSheet("color: #FFFFFF;font-size: 20px; font-weight: bold;")
        layout_tickets.addWidget(titulo_pcCambiar , 4, 4, 1, 1, alignment= Qt.AlignRight|Qt.AlignBottom)

        combobox_pc = QComboBox()
        combobox_pc.addItems(['1', '2'])
        combobox_pc.setFixedWidth(50)
        combobox_pc.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 20px;")
        layout_tickets.addWidget(combobox_pc,4, 5, 1, 1, alignment=Qt.AlignLeft |Qt.AlignBottom)

        boton_guardarPc = QPushButton('GUARDAR')
        boton_guardarPc.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_tickets.addWidget(boton_guardarPc,5, 4, 1, 2,
                                alignment=Qt.AlignTop| Qt.AlignHCenter)

        titulo_tablaOrdenDeLlegada = QLabel('ORDEN DE LLENADO')
        titulo_tablaOrdenDeLlegada.setStyleSheet("color: #FFFFFF;font-size: 40px; font-weight: bold;")
        layout_tickets.addWidget(titulo_tablaOrdenDeLlegada, 1, 6, 1, 3, alignment= Qt.AlignCenter |Qt.AlignTop)

        tabla_tablaOrdenDeLlegada = QTableWidget(self)
        tabla_tablaOrdenDeLlegada.setColumnCount(3)  # Definir el número de columnas
        tabla_tablaOrdenDeLlegada.setHorizontalHeaderLabels(
            ['NUMERO', 'ESTADO', 'PC'])
        tabla_tablaOrdenDeLlegada.setStyleSheet("""
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
        header = tabla_tablaOrdenDeLlegada.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        layout_tickets.addWidget(tabla_tablaOrdenDeLlegada, 2, 6, 5, 3)

        boton_subir = QPushButton('SUBIR')
        boton_subir.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_tickets.addWidget(boton_subir, 2, 9, 1, 1,
                                alignment=Qt.AlignTop| Qt.AlignHCenter)
        boton_bajar = QPushButton('BAJAR')
        boton_bajar.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_tickets.addWidget(boton_bajar, 2, 9, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        
        boton_guardar = QPushButton('GUARDAR')
        boton_guardar.setStyleSheet("color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;")
        layout_tickets.addWidget(boton_guardar,7, 6, 2, 3,
                                alignment=Qt.AlignCenter| Qt.AlignHCenter)
  
        page_casilleros.setLayout(layout_tickets)

        layout_tickets.setRowStretch(0, 0)
        layout_tickets.setRowStretch(1, 1)
        layout_tickets.setRowStretch(2, 1)
        layout_tickets.setRowStretch(3, 1)
        layout_tickets.setRowStretch(4, 1)
        layout_tickets.setRowStretch(5, 1)
        layout_tickets.setRowStretch(6, 1)
        layout_tickets.setRowStretch(7, 1)
        layout_tickets.setRowStretch(8, 1)
        self.stacked_widget.addWidget(page_casilleros)
