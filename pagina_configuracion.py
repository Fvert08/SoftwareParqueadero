from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout,QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtCore import QDate, Qt
import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QDateEdit, QGridLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
class PaginaConfiguracion(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        # Crear el widget de la página de registros
        page_cronfiguracion = QWidget()

        # Crear un layout para organizar los elementos en la página
        layout_cronfiguracion = QGridLayout()

        titulo_casilleros = QLabel('CONFIGURACION')
        titulo_casilleros.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_cronfiguracion.addWidget(titulo_casilleros, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_cronfiguracion.addWidget(linea_horizontal1, 0, 0, 1, 7, alignment=Qt.AlignBottom)

        #Se agrega el layout a la pagina
        page_cronfiguracion.setLayout(layout_cronfiguracion)
        #Se agrega al stack
        self.stacked_widget.addWidget(page_cronfiguracion)