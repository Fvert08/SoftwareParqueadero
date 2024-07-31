from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout,QHeaderView,QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtCore import QDate, Qt
import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QDateEdit, QGridLayout, QVBoxLayout, QWidget, QAbstractItemView
from PyQt5.QtCore import Qt
from config import DB_CONFIG
from DatabaseConnection import DatabaseConnection
from datetime import datetime, date
class PaginaReportes(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def actualizarTablaRegistros(self,tabla_registros):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        datosTablaRegistros = db_connection.cargarTableRegistros()
        self.tabla_registros.setRowCount(len(datosTablaRegistros))
        for row_idx, registro in enumerate(datosTablaRegistros):
            
            item_id = QTableWidgetItem(str(registro['id']))
            item_id.setTextAlignment(Qt.AlignCenter)
            tabla_registros.setItem(row_idx, 0, item_id)
            
            item_Fecha = QTableWidgetItem(registro['Fecha'].strftime('%Y-%m-%d') if isinstance(registro['Fecha'], (datetime, date)) else str(registro['Fecha']))
            item_Fecha.setTextAlignment(Qt.AlignCenter)
            tabla_registros.setItem(row_idx, 1, item_Fecha)
            
            item_hora = QTableWidgetItem(str(registro.get('Hora')))
            item_hora.setTextAlignment(Qt.AlignCenter)
            tabla_registros.setItem(row_idx, 2, item_hora)

            item_Tipo = QTableWidgetItem(str(registro['Tipo']))
            item_Tipo.setTextAlignment(Qt.AlignCenter)
            tabla_registros.setItem(row_idx, 3, item_Tipo)

            item_FechaInicio = QTableWidgetItem(registro['fechaInicio'].strftime('%Y-%m-%d') if isinstance(registro['fechaInicio'], (datetime, date)) else str(registro['fechaInicio']))
            item_FechaInicio.setTextAlignment(Qt.AlignCenter)
            tabla_registros.setItem(row_idx, 4, item_FechaInicio)

            item_FechaFin = QTableWidgetItem(registro['fechaFin'].strftime('%Y-%m-%d') if isinstance(registro['fechaFin'], (datetime, date)) else str(registro['fechaFin']))
            item_FechaFin.setTextAlignment(Qt.AlignCenter)
            tabla_registros.setItem(row_idx, 5, item_FechaFin)

            item_Registros = QTableWidgetItem(str(registro['registrosMotosHora']))
            item_Registros.setTextAlignment(Qt.AlignCenter)
            tabla_registros.setItem(row_idx, 6, item_Registros)

            item_DineroTotal = QTableWidgetItem(str(registro['totalMotosHora']))
            item_DineroTotal.setTextAlignment(Qt.AlignCenter)
            tabla_registros.setItem(row_idx, 7, item_DineroTotal)

    def initUI(self):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Crear el widget de la página de registros
        page_reportes = QWidget()

        # Crear un layout para organizar los elementos en la página
        layout_reportes = QGridLayout()

        titulo_casilleros = QLabel('GESTIONAR REPORTES')
        titulo_casilleros.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_reportes.addWidget(titulo_casilleros, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_reportes.addWidget(linea_horizontal1, 0, 0, 1, 7, alignment=Qt.AlignBottom)
        #Titulo
        titulo_tablaReportes = QLabel('Historial de reportes')
        titulo_tablaReportes.setStyleSheet("color: #FFFFFF;font-size: 40px; font-weight: bold;")
        layout_reportes.addWidget(titulo_tablaReportes, 1, 2, 1, 1, alignment= Qt.AlignCenter |Qt.AlignBottom)
        #Tabla
        self.tabla_registros = QTableWidget(self)
        self.tabla_registros.setColumnCount(8)  # Definir el número de columnas
        self.tabla_registros.verticalHeader().setVisible(False)
        self.tabla_registros.setHorizontalHeaderLabels(
            ['ID', 'Tipo', 'Desde','Hasta','Fecha generación','Hora generación','Registros','Total'])
        self.tabla_registros.setStyleSheet("""
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
        #seleccionar toda la fila
        self.tabla_registros.setSelectionBehavior(QAbstractItemView.SelectRows)

        header = self.tabla_registros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        layout_reportes.addWidget(self.tabla_registros, 2, 0, 8, 5)

        # Rellenar la tabla
        self.actualizarTablaRegistros(self.tabla_registros)
        # Crea un boton para Reimprimir
        boton_reimprimir = QPushButton('Reimprimir')
        boton_reimprimir.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
        layout_reportes.addWidget(boton_reimprimir, 10, 4, 1, 1,
                                alignment=Qt.AlignTop| Qt.AlignRight)
        
        
        #Formulario
        # Crear el label "ID" y la textbox
        label_id = QLabel('ID')
        label_id.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_reportes.addWidget(label_id, 2, 5, 1, 1, alignment=Qt.AlignTop | Qt.AlignRight)
        # Text box ID
        textbox_id = QLineEdit()
        textbox_id.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_id.setFixedWidth(240)
        layout_reportes.addWidget(textbox_id, 3, 5, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)
        textbox_id.setReadOnly(True)
        # Crear el label "reportar" y la textbox
        label_reportar = QLabel('Reportar')
        label_reportar.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_reportes.addWidget(label_reportar, 4, 5, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)
        # combobox box reportar
        combobox_reportar= QComboBox()
        combobox_reportar.addItems(['Todo', 'Hora', 'Dia', 'Mes'])
        combobox_reportar.setFixedWidth(240)
        combobox_reportar.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 40px;")
        layout_reportes.addWidget(combobox_reportar, 5, 5, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear el label "Desde" y la textbox
        label_desde = QLabel('Desde')
        label_desde.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_reportes.addWidget(label_desde, 6, 5, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)
       # Date desde
        date_desde = QDateEdit()
        date_desde.setFixedWidth(240)
        date_desde.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 40px;")
        date_desde.setCalendarPopup(True)  # Habilitar el popup de calendario
        date_desde.setDate(QDate.currentDate())  # Establecer la fecha actual
        date_desde.setMaximumDate(QDate.currentDate())  # Establecer la fecha máxima permitida como la fecha actual
        calendarDesde_widget = date_desde.calendarWidget()
        calendarDesde_widget.setStyleSheet("font-size: 20px;") 
        calendarDesde_widget.setStyleSheet("background-color: #222126; color: white; font-size: 20px; alternate-background-color: #131216;")
        layout_reportes.addWidget(date_desde, 7, 5, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)
        # Crear el label "Hasta" y la textbox
        label_hasta = QLabel('Hasta')
        label_hasta.setStyleSheet("color: #FFFFFF;font-size: 40px;")
        layout_reportes.addWidget(label_hasta, 8, 5, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)
       # Date hasta
        date_hasta = QDateEdit()
        date_hasta.setFixedWidth(240)
        date_hasta.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 40px;")
        date_hasta.setCalendarPopup(True)  # Habilitar el popup de calendario
        date_hasta.setDate(QDate.currentDate())  # Establecer la fecha actual
        date_hasta.setMaximumDate(QDate.currentDate())  # Establecer la fecha máxima permitida como la fecha actual
        calendarhasta_widget = date_hasta.calendarWidget()
        calendarhasta_widget.setStyleSheet("font-size: 20px;") 
        calendarhasta_widget.setStyleSheet("background-color: #222126; color: white; font-size: 20px; alternate-background-color: #131216;")
        layout_reportes.addWidget(date_hasta, 9, 5, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)
        page_reportes.setLayout(layout_reportes)
        self.stacked_widget.addWidget(page_reportes)

        # Crea un boton para Reimprimir
        boton_imprimir = QPushButton('Imprimir')
        boton_imprimir.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
        layout_reportes.addWidget(boton_imprimir, 10, 5, 1, 2,
                                alignment=Qt.AlignTop| Qt.AlignCenter)
         # Conectar el botón de imprimir a la función registrarMoto
        boton_imprimir.clicked.connect(lambda: [
            db_connection.consultarReporte(
                date_desde.text(),
                date_hasta.text(),
        ),
        #self.senalActualizarTablaRegistroMotos.emit()
        ])

        layout_reportes.setRowStretch(0, 0)
        layout_reportes.setRowStretch(1, 1)
        layout_reportes.setRowStretch(2, 1)
        layout_reportes.setRowStretch(3, 1)
        layout_reportes.setRowStretch(4, 1)
        layout_reportes.setRowStretch(5, 1)
        layout_reportes.setRowStretch(6, 1)
        layout_reportes.setRowStretch(7, 1)
        layout_reportes.setRowStretch(8, 1)
        layout_reportes.setRowStretch(9, 1)
        layout_reportes.setRowStretch(10, 1)

        page_reportes.setLayout(layout_reportes)
        self.stacked_widget.addWidget(page_reportes)

