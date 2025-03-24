from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout,QHeaderView
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtCore import QDate, Qt
import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QDateEdit, QGridLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
class PaginaCreditos(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        # Crear el widget de la página de registros
        page_creditos = QWidget()

        # Crear un layout para organizar los elementos en la página
        layout_creditos = QGridLayout()

        titulo_casilleros = QLabel('CREDITOS')
        titulo_casilleros.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_creditos.addWidget(titulo_casilleros, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_creditos.addWidget(linea_horizontal1, 1, 0, 1, 7)

        titulo_principal = QLabel('SOFTWARE DESAROLLADO POR')
        titulo_principal.setStyleSheet("color: #FFFFFF;font-size: 40px; font-weight: bold;")
        layout_creditos.addWidget(titulo_principal, 2, 0, 1, 7, alignment= Qt.AlignHCenter |Qt.AlignBottom)

        titulo_nombre1 = QLabel('JAVIER PARRA')
        titulo_nombre1 .setStyleSheet("color: #FFFFFF;font-size: 40px; font-weight: bold;")
        layout_creditos.addWidget(titulo_nombre1 , 3, 0, 1, 7, alignment= Qt.AlignHCenter |Qt.AlignBottom)
        
        titulo_nombre2 = QLabel('JUAN LOAIZA')
        titulo_nombre2 .setStyleSheet("color: #FFFFFF;font-size: 40px; font-weight: bold;")
        layout_creditos.addWidget(titulo_nombre2 , 4, 0, 1, 7, alignment= Qt.AlignHCenter |Qt.AlignCenter)

        titulo_carrera = QLabel('ESTUDIANTES DE INGENIERIA EN SISTEMAS')
        titulo_carrera .setStyleSheet("color: #FFFFFF;font-size: 20px; font-weight: bold;")
        layout_creditos.addWidget(titulo_carrera, 5, 0, 1, 7, alignment= Qt.AlignHCenter |Qt.AlignBottom)

        titulo_universidad = QLabel('UTP')
        titulo_universidad.setStyleSheet("color: #FFFFFF;font-size: 20px; font-weight: bold;")
        layout_creditos.addWidget(titulo_universidad, 6, 0, 1, 7, alignment= Qt.AlignHCenter |Qt.AlignCenter)

        titulo_contacto = QLabel('CONTACTO Y SOPORTE')
        titulo_contacto .setStyleSheet("color: #FFFFFF;font-size: 40px; font-weight: bold;")
        layout_creditos.addWidget(titulo_contacto , 7, 0, 1, 7, alignment= Qt.AlignHCenter |Qt.AlignBottom)

        titulo_numero1 = QLabel('3192742428')
        titulo_numero1 .setStyleSheet("color: #FFFFFF;font-size: 40px; font-weight: bold;")
        layout_creditos.addWidget(titulo_numero1 , 8, 0, 1, 7, alignment= Qt.AlignHCenter |Qt.AlignBottom)
        
        titulo_numero2 = QLabel('3246844088')
        titulo_numero2 .setStyleSheet("color: #FFFFFF;font-size: 40px; font-weight: bold;")
        layout_creditos.addWidget(titulo_numero2 , 9, 0, 1, 7, alignment= Qt.AlignHCenter |Qt.AlignCenter)

        #Crear un QLabel para mostrar la imagen
        label_Logo = QLabel(self)
        
        # Crear un QPixmap con la ruta de la imagen
        pixmapLogo = QPixmap('imagenes/LogoJDEV.png')
        
        # Escalar el QPixmap al tamaño deseado (30x30 píxeles) manteniendo la proporción
        scaled_pixmapLogo = pixmapLogo.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Establecer el QPixmap escalado en el QLabel
        label_Logo.setPixmap(scaled_pixmapLogo)
        # Ajustar el tamaño del QLabel al tamaño de la imagen escalada
        label_Logo.setFixedSize(200, 200)
        layout_creditos.addWidget(label_Logo , 8, 6, 2, 1, alignment= Qt.AlignRight |Qt.AlignBottom)

        layout_creditos.setRowStretch(0, 0)
        layout_creditos.setRowStretch(1, 1)
        layout_creditos.setRowStretch(2, 1)
        layout_creditos.setRowStretch(3, 1)
        layout_creditos.setRowStretch(4, 1)
        layout_creditos.setRowStretch(5, 1)
        layout_creditos.setRowStretch(6, 1)
        layout_creditos.setRowStretch(7, 1)
        layout_creditos.setRowStretch(8, 1)
        layout_creditos.setRowStretch(9, 1)
        #Se agrega el layout a la pagina
        page_creditos.setLayout(layout_creditos)
        #Se agrega al stack

        self.stacked_widget.addWidget(page_creditos)