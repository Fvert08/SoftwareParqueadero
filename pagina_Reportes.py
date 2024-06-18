from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
class PaginaReportes(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        # Crear el widget de la página de registros
        page_reportes = QWidget()

        # Crear un layout para organizar los elementos en la página
        layout_reportes = QVBoxLayout(page_reportes)

        # Crear el título "Registros"
        titulo_tickets = QLabel('Gestionar Reportes', page_reportes)
        titulo_tickets.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_reportes.addWidget(titulo_tickets, alignment=Qt.AlignCenter)
        self.stacked_widget.addWidget(page_reportes)
