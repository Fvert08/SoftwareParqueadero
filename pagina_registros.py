from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
class PaginaRegistros(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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