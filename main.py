from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout
from PyQt5.QtGui import QIcon , QPixmap
from PyQt5.QtCore import Qt,QSize
import sys
from pagina_registros import PaginaRegistros
from pagina_Tickets import PaginaTickets
from pagina_Casilleros import PaginaCasilleros
from pagina_Reportes import PaginaReportes
from pagina_configuracion import PaginaConfiguracion
from pagina_creditos import PaginaCreditos
from PyQt5.QtGui import QScreen
class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SOFTWARE PARQUEADERO')
        self.setStyleSheet("background-color: #151419;")
        # Obtener el tamaño de la pantalla del usuario
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.width = screen_size.width()
        self.height = screen_size.height()
        self.setWindowState(Qt.WindowMaximized)
        self.setMaximumSize(self.width, self.height)  # tamaño máximo igual al tamaño de la pantalla
        self.Pagina_principal()

    def Pagina_principal(self):
         # Crear un QLabel para mostrar la imagen
        label_Logo = QLabel(self)
        
        # Crear un QPixmap con la ruta de la imagen
        pixmapLogo = QPixmap('LogoJDEV.png')
        
        # Escalar el QPixmap al tamaño deseado (30x30 píxeles) manteniendo la proporción
        scaled_pixmapLogo = pixmapLogo.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Establecer el QPixmap escalado en el QLabel
        label_Logo.setPixmap(scaled_pixmapLogo)
        
        # Ajustar el tamaño del QLabel al tamaño de la imagen escalada
        label_Logo.setFixedSize(100, 100)

        main_layout = QHBoxLayout(self)

        # Creando el menú de la izquierda
        menuizquierdo = QWidget()
        layout_menu = QVBoxLayout(menuizquierdo)
        layout_menu.addWidget (label_Logo,alignment=Qt.AlignCenter)
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
        layout_menu.addWidget(self.botonRegistros, alignment=Qt.AlignCenter)

        self.botontickets = QPushButton('Generar Tickets', self)
        self.botontickets.setStyleSheet("background-color: #151419; color: #737074; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        self.botontickets.setIcon(QIcon('ticketMotos.png'))
        self.botontickets.setCheckable(True)
        self.botontickets.pressed.connect(self.cambiar_color)
        layout_menu.addWidget(self.botontickets, alignment=Qt.AlignCenter)

        self.botonGestionarCasilleros = QPushButton('Gestionar casilleros', self)
        self.botonGestionarCasilleros.setStyleSheet("background-color: #151419; color: #737074; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        self.botonGestionarCasilleros.setIcon(QIcon('gestionCasilleros.png'))
        self.botonGestionarCasilleros.setCheckable(True)
        self.botonGestionarCasilleros.pressed.connect(self.cambiar_color)
        layout_menu.addWidget(self.botonGestionarCasilleros, alignment=Qt.AlignCenter)

        self.botonReportes = QPushButton('Gestión de reportes', self)
        self.botonReportes.setStyleSheet("background-color: #151419; color: #737074; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        self.botonReportes.setIcon(QIcon('reportes.png'))
        self.botonReportes.setCheckable(True)
        self.botonReportes.pressed.connect(self.cambiar_color)
        layout_menu.addWidget(self.botonReportes, alignment=Qt.AlignCenter)

        self.botonConfiguracion = QPushButton('Configuracion', self)
        self.botonConfiguracion.setStyleSheet("background-color: #151419; color: #737074; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        self.botonConfiguracion.setIcon(QIcon('Configuracion.png'))
        self.botonConfiguracion.setCheckable(True)
        self.botonConfiguracion.pressed.connect(self.cambiar_color)
        layout_menu.addWidget(self.botonConfiguracion, alignment=Qt.AlignCenter)

        self.botonConCreditos = QPushButton('Creditos', self)
        self.botonConCreditos.setStyleSheet("background-color: #151419; color: #737074; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;")
        self.botonConCreditos.setIcon(QIcon('LogoJDev.png'))
        self.botonConCreditos.setCheckable(True)
        self.botonConCreditos.pressed.connect(self.cambiar_color)
        layout_menu.addWidget(self.botonConCreditos, alignment=Qt.AlignCenter)

        layout_menu.setAlignment(Qt.AlignTop)
        #Se crea el stacked widget
        self.stacked_widget = QStackedWidget(self)
        #agrega al layout el menú y el stack
        main_layout.addWidget(menuizquierdo)
        main_layout.addWidget(self.stacked_widget)
        # Se captura el ultimo boton seleccionado
        self.ultimo_boton_seleccionado = self.botonRegistros
        # se setea el layout principal 
        self.setLayout(main_layout)
        # Crear instancias de las páginas y agregarlas al QStackedWidget
        self.pagina_registros = PaginaRegistros(self.stacked_widget)
        self.stacked_widget.addWidget(self.pagina_registros)

        self.pagina_tickets = PaginaTickets(self.stacked_widget)
        self.stacked_widget.addWidget(self.pagina_tickets)

        self.pagina_casilleros = PaginaCasilleros(self.stacked_widget)
        self.stacked_widget.addWidget(self.pagina_casilleros)

        self.pagina_reportes = PaginaReportes(self.stacked_widget)
        self.stacked_widget.addWidget(self.pagina_reportes)

        self.pagina_configuracion = PaginaConfiguracion(self.stacked_widget)
        self.stacked_widget.addWidget(self.pagina_configuracion)

        self.pagina_creditos = PaginaCreditos(self.stacked_widget)
        self.stacked_widget.addWidget(self.pagina_creditos)

        

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
            self.setMinimumSize(int(self.width-(self.width/4)), int(self.height-(self.height/2)))  # tamaño mínimo
        elif sender.text() == "Generar Tickets":
            self.stacked_widget.setCurrentIndex(2)
            self.setMinimumSize(int(self.width-(self.width/7)), int(self.height-(self.height/2)))  # tamaño mínimo
        elif sender.text() == "Gestionar casilleros":
            self.stacked_widget.setCurrentIndex(4)
        elif sender.text() == "Gestión de reportes":
            self.stacked_widget.setCurrentIndex(6)
        elif sender.text() == "Configuracion":
            self.stacked_widget.setCurrentIndex(8)
        elif sender.text() == "Creditos":
            self.stacked_widget.setCurrentIndex(10)

# Iniciar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())
