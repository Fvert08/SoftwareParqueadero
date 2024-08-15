from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout,QHeaderView,QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtCore import QDate, Qt
import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QDateEdit, QGridLayout, QVBoxLayout, QWidget, QAbstractItemView
from PyQt5.QtCore import Qt
from config import DB_CONFIG
from DatabaseConnection import DatabaseConnection
from generarTickets.TicketReporte import generarTicketReporteCompleto
from datetime import datetime, date
from PyQt5.QtCore import pyqtSignal
class PaginaReportes(QWidget):
    senalActualizarTablaReportes = pyqtSignal()
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def actualizarTablaRegistros(self):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        datosTablaRegistros = db_connection.cargarTableRegistros()
        self.tabla_registros.setRowCount(len(datosTablaRegistros))
        for row_idx, registro in enumerate(datosTablaRegistros):
            
            item_id = QTableWidgetItem(str(registro['id']))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 0, item_id)
            
            item_Fecha = QTableWidgetItem(registro['Fecha'].strftime('%Y-%m-%d') if isinstance(registro['Fecha'], (datetime, date)) else str(registro['Fecha']))
            item_Fecha.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 1, item_Fecha)
            
            item_hora = QTableWidgetItem(str(registro.get('Hora')))
            item_hora.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 2, item_hora)

            item_Tipo = QTableWidgetItem(str(registro['Tipo']))
            item_Tipo.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 3, item_Tipo)

            item_FechaInicio = QTableWidgetItem(registro['fechaInicio'].strftime('%Y-%m-%d') if isinstance(registro['fechaInicio'], (datetime, date)) else str(registro['fechaInicio']))
            item_FechaInicio.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 4, item_FechaInicio)

            item_FechaFin = QTableWidgetItem(registro['fechaFin'].strftime('%Y-%m-%d') if isinstance(registro['fechaFin'], (datetime, date)) else str(registro['fechaFin']))
            item_FechaFin.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 5, item_FechaFin)

            item_RegistrosMotosHora = QTableWidgetItem(str(registro['registrosMotosHora']))
            item_RegistrosMotosHora.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 6, item_RegistrosMotosHora)

            item_DineroTotalMotosHora = QTableWidgetItem(str(registro['totalMotosHora']))
            item_DineroTotalMotosHora.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 7, item_DineroTotalMotosHora)

            item_RegistrosMotosDia = QTableWidgetItem(str(registro['registrosMotosDia']))
            item_RegistrosMotosDia.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 8, item_RegistrosMotosDia)

            item_DineroTotalMotosDia = QTableWidgetItem(str(registro['totalMotosDia']))
            item_DineroTotalMotosDia.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 9, item_DineroTotalMotosDia)

            item_RegistrosMotosMes = QTableWidgetItem(str(registro['registrosMotosMes']))
            item_RegistrosMotosMes.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 10, item_RegistrosMotosMes)

            item_DineroTotalMotosMes = QTableWidgetItem(str(registro['totalMotosMes']))
            item_DineroTotalMotosMes.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 11, item_DineroTotalMotosMes)

            item_RegistrosMotosFijos = QTableWidgetItem(str(registro['registrosFijos']))
            item_RegistrosMotosFijos.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 12, item_RegistrosMotosFijos)

            item_DineroTotalMotosFijos = QTableWidgetItem(str(registro['totalFijos']))
            item_DineroTotalMotosFijos.setTextAlignment(Qt.AlignCenter)
            self.tabla_registros.setItem(row_idx, 13, item_DineroTotalMotosFijos)

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
        self.tabla_registros.setColumnCount(14)  # Definir el número de columnas
        self.tabla_registros.verticalHeader().setVisible(False)
        self.tabla_registros.setHorizontalHeaderLabels(
            ['ID', 'Fecha.G', 'Hora.G','Tipo','Fecha.I','Fecha.F','Reg.M.Hora','Total.M.Hora','Reg.M.Dia','Total.M.Dia','Reg.M.Mes','Total.M.Mes','Reg.F','Total.F'])
        self.tabla_registros.setStyleSheet("""
                  QTableWidget {
                background-color: #222126;
                color: white;
                border: 1px solid #222126;
                alternate-background-color: #131216; /* Color de fila alternativa */
            }

            QTableWidget::item {
                background-color: #151419; /* Color de fondo de las celdas */
                border: 0px solid #222126; /* Color y ancho del borde de las celdas */
            }

            QTableWidget::item:hover {
                background-color: #2a292e; /* Color de fondo al pasar el mouse sobre una celda */
            }

            QTableWidget::item:selected {
                background-color: #3c3b40; /* Color de fondo al seleccionar una celda */
                color: white; /* Color del texto de la celda seleccionada */
            }

            QHeaderView::section {
                background-color: #151419; /* Color de fondo de las cabeceras de las columnas */
                color: white; /* Color del texto de las cabeceras de las columnas */
                border: none; /* Sin borde */
                padding: 4px; /* Ajuste del relleno */
            }

            QHeaderView::section:hover {
                background-color: #2a292e; /* Color de fondo al pasar el mouse */
            }

            QHeaderView::section:selected {
                background-color: white; /* Color de fondo al seleccionar */
                color: white; /* Color del texto de las cabeceras de las columnas */
            }

            QLineEdit {
                color: white; /* Color del texto del QLineEdit durante la edición */
            }
                """)
        header = self.tabla_registros.horizontalHeader()
        #seleccionar toda la fila
        self.tabla_registros.setSelectionBehavior(QAbstractItemView.SelectRows)

        header = self.tabla_registros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        
        #se configuran las propiedades de latabla, para que se seleccione toda la fila y no se permita editar
        self.tabla_registros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_registros.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout_reportes.addWidget(self.tabla_registros, 2, 0, 8, 5)

        # Rellenar la tabla
        self.actualizarTablaRegistros()
        # Crea un boton para Reimprimir
        boton_reimprimir = QPushButton('Reimprimir')
        boton_reimprimir.setStyleSheet(
            "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 15px 30px;")
        layout_reportes.addWidget(boton_reimprimir, 10, 4, 1, 1,
                                alignment=Qt.AlignTop| Qt.AlignRight)
        boton_reimprimir.clicked.connect(lambda: [
            generarTicketReporteCompleto(
            self.tabla_registros.item(self.tabla_registros.currentRow(), 0).text(),
            "COPIA",
            self.tabla_registros.item(self.tabla_registros.currentRow(), 1).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 2).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 4).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 5).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 6).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 7).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 8).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 9).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 10).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 11).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 12).text(),
            self.tabla_registros.item(self.tabla_registros.currentRow(), 13).text(),
        ),
        self.senalActualizarTablaReportes.emit()
        ])
        
        #Formulario
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
        date_desde.setDisplayFormat("yyyy-MM-dd")
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
        date_hasta.setDisplayFormat("yyyy-MM-dd")
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
                "ORIGINAL"
        ),
            date_desde.setMaximumDate(QDate.currentDate()),
            date_hasta.setDate(QDate.currentDate()),
            self.actualizarTablaRegistros()

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

