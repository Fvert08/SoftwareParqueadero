from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QStackedWidget, QComboBox, QLineEdit, QGridLayout, QCheckBox, QTableWidget, QHBoxLayout, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtCore import QDate, Qt
import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QDateEdit, QGridLayout, QVBoxLayout, QWidget, QAbstractItemView
from PyQt5.QtCore import Qt
from config import DB_CONFIG
from DatabaseConnection import DatabaseConnection
from FileEnCo import generarCodigoEncriptado
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from datetime import datetime, date
from PyQt5.QtCore import pyqtSignal
from leerTxt import escribir_archivo
from leerTxt import leer_archivo

class PaginaConfiguracion(QWidget):
    senalActualizarTextboxesSuscripcion = pyqtSignal()
    senalActualizarTablaPCs= pyqtSignal()
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def actualizarComboboxpcs (self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        ids = db_connection.obtenerIdsRegPc()
        self.combobox_pc.clear()
        self.combobox_pc.addItems(map(str, ids))

    def actualizarTablaUsuarios(self):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        datosTablaUsuarios = db_connection.cargarTableUsuarios()
        self.tabla_Usuarios.setRowCount(len(datosTablaUsuarios))
        for row_idx, registro in enumerate(datosTablaUsuarios):
            
            item_id = QTableWidgetItem(str(registro['id']))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tabla_Usuarios.setItem(row_idx, 0, item_id)
            
            item_Usuario = QTableWidgetItem(str(registro['Usuario']))
            item_Usuario.setTextAlignment(Qt.AlignCenter)
            self.tabla_Usuarios.setItem(row_idx, 1, item_Usuario)
            
            item_Contrasena = QTableWidgetItem(str(registro['Contrasena']))
            item_Contrasena.setTextAlignment(Qt.AlignCenter)
            self.tabla_Usuarios.setItem(row_idx, 2, item_Contrasena)

            item_Tipo = QTableWidgetItem(str(registro['Tipo']))
            item_Tipo.setTextAlignment(Qt.AlignCenter)
            self.tabla_Usuarios.setItem(row_idx, 3, item_Tipo)

    def actualizarTablaPCAgregados(self):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        datosTablaPCAgregados = db_connection.cargarTablePCAgregados()
        self.tabla_PCAgregados.setRowCount(len(datosTablaPCAgregados))
        for row_idx, registro in enumerate(datosTablaPCAgregados):
            
            item_id = QTableWidgetItem(str(registro['id']))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tabla_PCAgregados.setItem(row_idx, 0, item_id)
            
            item_Descripcion = QTableWidgetItem(str(registro['Descripcion']))
            item_Descripcion.setTextAlignment(Qt.AlignCenter)
            self.tabla_PCAgregados.setItem(row_idx, 1, item_Descripcion)

            pc_value = registro['id']
            cantidad = db_connection.contarTablePCAgregados(pc_value) 
            item_ContarPc = QTableWidgetItem(str(cantidad))
            item_ContarPc.setTextAlignment(Qt.AlignCenter)
            self.tabla_PCAgregados.setItem(row_idx, 2, item_ContarPc)

    def initUI(self):
        #----Paginas
        #Pagina del Principal
        page_configuracion = QWidget()
        #Pagina del menú
        page_configuracionMenu = QWidget()
        
        # -----Stack para agregar todas las pantallas de tickets
        self.stacked_widgetConfiguracion = QStackedWidget()

        #--------#layouts (Izquierdo, derecho y principal)
        #layout Menu derecho donde se agregan todos los botones
        layout_configuracion = QGridLayout()
        
        #layout principal box horizontal
        main_layoutConfiguracion = QHBoxLayout()

        #Se llaman las pantallas para cargarlas en el stack
        self.pantallaValoresFacturacion()
        self.pantallaValidarAcceso()
        self.pantallaPC()
        self.pantallaSuscripcion()
        
        #------------------------Menu lateral---------------------------
        # Crear la línea vertical de 1 pixel y añadirla a la cuadrícula
        linea_vertical = QFrame()
        linea_vertical.setFrameShape(QFrame.VLine)
        linea_vertical.setLineWidth(1)
        linea_vertical.setStyleSheet("color: #FFFFFF;")
        layout_configuracion.addWidget(linea_vertical, 0, 0, 8, 1)

        # Crear la sección derecha con el título "Menú"
        titulo_menu = QLabel('Menú')
        titulo_menu.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_configuracion.addWidget(titulo_menu, 0, 1, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)

        linea_horizontal2 = QFrame()
        linea_horizontal2.setFrameShape(QFrame.HLine)
        linea_horizontal2.setLineWidth(1)
        linea_horizontal2.setStyleSheet("color: #FFFFFF;")
        layout_configuracion.addWidget(linea_horizontal2, 0, 1, 1, 2, alignment=Qt.AlignBottom)

        layout_configuracion.setRowStretch(0, 0)
        layout_configuracion.setRowStretch(1, 1)
        layout_configuracion.setRowStretch(2, 1)
        layout_configuracion.setRowStretch(3, 1)
        layout_configuracion.setRowStretch(4, 1)
        layout_configuracion.setRowStretch(5, 1)
        layout_configuracion.setRowStretch(6, 1)

        # Crea un boton para cambiar a las configuraciones de Usuario
        boton_Usuarios = QPushButton("VALORES")
        boton_Usuarios.setStyleSheet("color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;")
        layout_configuracion.addWidget(boton_Usuarios, 1, 1, 1, 1, alignment=Qt.AlignHCenter  | Qt.AlignCenter)
        boton_Usuarios.clicked.connect(lambda: self.stacked_widgetConfiguracion.setCurrentIndex(0))

        # Crea un boton para cambiar a las configuraciones de Conexión
        boton_Conexion = QPushButton("VALIDAR")
        boton_Conexion.setStyleSheet("color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;")
        layout_configuracion.addWidget(boton_Conexion, 2, 1, 1, 1, alignment=Qt.AlignHCenter | Qt.AlignCenter)
        boton_Conexion.clicked.connect(lambda: self.stacked_widgetConfiguracion.setCurrentIndex(1))
        
         # Crea un boton para cambiar a las configuraciones de PC
        boton_PC = QPushButton("PC")
        boton_PC.setStyleSheet("color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;")
        layout_configuracion.addWidget(boton_PC, 3, 1, 1, 1, alignment=Qt.AlignHCenter  |Qt.AlignCenter)
        boton_PC.clicked.connect(lambda: self.stacked_widgetConfiguracion.setCurrentIndex(2))  

         # Crea un boton para cambiar a la suscripcion del PC
        boton_Suscripcion = QPushButton("SUSCRIPCIÓN")
        boton_Suscripcion.setStyleSheet("color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;")
        layout_configuracion.addWidget(boton_Suscripcion, 4, 1, 1, 1, alignment=Qt.AlignHCenter  |Qt.AlignCenter)
        boton_Suscripcion.clicked.connect(lambda: self.stacked_widgetConfiguracion.setCurrentIndex(3))  
        
        #Se agrega el layout a la pagina
        page_configuracionMenu.setLayout(layout_configuracion)
        #Se agrega el stack al layout principal
        main_layoutConfiguracion.addWidget(self.stacked_widgetConfiguracion)
        #se agrega el menú al layout principal
        main_layoutConfiguracion.addWidget(page_configuracionMenu)
        #se agrega el layout principal a la pagina principal
        page_configuracion.setLayout(main_layoutConfiguracion)
        #se llama la primera posición del stack
        self.stacked_widgetConfiguracion.setCurrentIndex(0)
        #Se agrega al stack
        self.stacked_widget.addWidget(page_configuracion)
    
    def pantallaValoresFacturacion(self):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        #Pagina de Usuarios
        page_Valores = QWidget()
        #Layout de la Pagina de Usuarios
        layout_Valores = QGridLayout()
        #------------------------------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_CambiarValores = QLabel('VALORES DE FACTURACION')
        titulo_CambiarValores.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_Valores.addWidget(titulo_CambiarValores, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_Valores.addWidget(linea_horizontal1, 1, 0, 1, 7)
        #Titulo
        titulo_usuariosAgregados = QLabel('Valores')
        titulo_usuariosAgregados .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_Valores.addWidget(titulo_usuariosAgregados  , 2, 0, 1, 7, alignment= Qt.AlignCenter |Qt.AlignHCenter)
   
        #Hora
        titulo_hora = QLabel('Hora')
        titulo_hora.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_Valores.addWidget(titulo_hora, 3, 1, 1, 2, alignment=Qt.AlignHCenter| Qt.AlignCenter)

        textbox_hora = QLineEdit()
        textbox_hora.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        layout_Valores.addWidget(textbox_hora, 3, 3, 1, 2, alignment=Qt.AlignHCenter |Qt.AlignCenter)
        #Dia
        titulo_dia = QLabel('Dia')
        titulo_dia.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_Valores.addWidget(titulo_dia, 4, 1, 1, 2, alignment=Qt.AlignHCenter| Qt.AlignCenter)

        textbox_dia = QLineEdit()
        textbox_dia.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        layout_Valores.addWidget(textbox_dia, 4, 3, 1, 2, alignment=Qt.AlignHCenter |Qt.AlignCenter)
        #Mes
        titulo_mes = QLabel('Mes')
        titulo_mes.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_Valores.addWidget(titulo_mes, 5, 1, 1, 2, alignment=Qt.AlignHCenter| Qt.AlignCenter)

        textbox_mes = QLineEdit()
        textbox_mes.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        layout_Valores.addWidget(textbox_mes, 5, 3, 1, 2, alignment=Qt.AlignHCenter |Qt.AlignCenter)

        boton_aceptar = QPushButton('ACEPTAR')
        boton_aceptar.setStyleSheet("color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;")
        layout_Valores.addWidget(boton_aceptar, 6, 0, 1, 7,
                                alignment=Qt.AlignHCenter| Qt.AlignCenter)


        #Fila-Tamaño
        layout_Valores.setRowStretch(0, 0)
        layout_Valores.setRowStretch(1, 1)
        layout_Valores.setRowStretch(2, 1)
        layout_Valores.setRowStretch(3, 1)
        layout_Valores.setRowStretch(4, 1)
        layout_Valores.setRowStretch(5, 1)
        layout_Valores.setRowStretch(6, 1)

        #Se agrega el layout a la pagina
        page_Valores.setLayout(layout_Valores)
        #se agrega la pagina al stack
        self.stacked_widgetConfiguracion.addWidget(page_Valores)

    def pantallaValidarAcceso(self):
        #Pagina de Usuarios
        page_Validar = QWidget()
        #Layout de la Pagina de Usuarios
        layout_Validar = QGridLayout()
        #------------------------------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_validar = QLabel('VALIDAR ACCESO')
        titulo_validar.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_Validar.addWidget(titulo_validar, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_Validar.addWidget(linea_horizontal1, 1, 0, 1, 7)

        
        titulo_ContraseñaAcceso = QLabel('CONTRASEÑA')
        titulo_ContraseñaAcceso .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_Validar.addWidget(titulo_ContraseñaAcceso  , 2, 0, 1, 7, alignment= Qt.AlignBottom |Qt.AlignHCenter)

        textbox_ContraseñaAcceso = QLineEdit()
        textbox_ContraseñaAcceso.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        layout_Validar.addWidget(textbox_ContraseñaAcceso, 3, 0, 1, 7, alignment=Qt.AlignHCenter |Qt.AlignCenter)

        # Crea un boton para ingresar a generar ticket ingresar moto
        boton_OcultarContraseña = QPushButton()
        boton_OcultarContraseña.setStyleSheet("color: White; background-color: #151419; font-size: 30px; border-radius: 1px; padding: 10px 10px;")
        boton_OcultarContraseña.setIcon(QIcon('imagenes/OcultarContraseña.png'))  # Establecer el icono
        boton_OcultarContraseña.setIconSize(QSize(50, 50))  # Establecer el tamaño del icono
        layout_Validar.addWidget(boton_OcultarContraseña, 3, 4, 1, 3, alignment=Qt.AlignHCenter |Qt.AlignCenter)
        #Falta Integrar Ocultar
        boton_OcultarContraseña.clicked.connect(lambda: print("Ocultar"))#Se comprueba que funciona el boton
        #Boton Validar
        boton_validar = QPushButton('VALIDAR')
        boton_validar.setStyleSheet("color: White; background-color: #222125; font-size: 35px; border-radius: 15px; padding: 10px 20px;")
        layout_Validar.addWidget(boton_validar,4, 0, 1, 7,alignment=Qt.AlignHCenter |Qt.AlignTop)

        #Fila-Tamaño
        layout_Validar.setRowStretch(0, 0)
        layout_Validar.setRowStretch(1, 1)
        layout_Validar.setRowStretch(2, 1)
        layout_Validar.setRowStretch(3, 1)
        layout_Validar.setRowStretch(4, 1)
        layout_Validar.setRowStretch(5, 1)

        #Se agrega el layout a la pagina
        page_Validar.setLayout(layout_Validar)
        #se agrega la pagina al stack
        self.stacked_widgetConfiguracion.addWidget(page_Validar)

    def pantallaPC(self):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        #Pagina de pc
        page_PC = QWidget()
        #Layout de la Pagina de pc
        layout_PC = QGridLayout()
        #------------------------------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_ = QLabel('PC')
        titulo_.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_PC.addWidget(titulo_, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_PC.addWidget(linea_horizontal1, 1, 0, 1, 7)
        # Crear el título y añadirlo a la sección izquierda
        titulo_PcAgregados= QLabel('PC´S AGREGADOS')
        titulo_PcAgregados.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_PC.addWidget(titulo_PcAgregados, 2, 0, 1, 4, alignment=Qt.AlignHCenter | Qt.AlignCenter)
        #Tabla
        self.tabla_PCAgregados = QTableWidget(self)
        self.tabla_PCAgregados.setColumnCount(3)  # Definir el número de columnas
        self.tabla_PCAgregados.verticalHeader().setVisible(False)
        self.tabla_PCAgregados.setHorizontalHeaderLabels(['ID', 'DESCRIPCIÓN', 'CASILLEROS\nASOCIADOS'])
        self.tabla_PCAgregados.setStyleSheet("""
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
        #seleccionar toda la fila
        self.tabla_PCAgregados.setSelectionBehavior(QAbstractItemView.SelectRows)

        header = self.tabla_PCAgregados.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        layout_PC.addWidget(self.tabla_PCAgregados, 3, 0, 4, 4)

        # Rellenar la tabla
        self.actualizarTablaPCAgregados()

        #Botones Tabla
        boton_editar = QPushButton('EDITAR')
        boton_editar .setStyleSheet("color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;")
        layout_PC.addWidget(boton_editar , 7, 0, 1, 2,
                                alignment=Qt.AlignHCenter| Qt.AlignCenter)
        boton_editar.clicked.connect(lambda: [
            # Validaciones
            QMessageBox.warning(None, "Advertencia", "No hay registros seleccionados.") 
            if not self.tabla_PCAgregados.selectedItems() else 
            QMessageBox.warning(None, "Advertencia", "Este pc tiene casilleros asociados.") 
            if str(self.tabla_PCAgregados.item(self.tabla_PCAgregados.currentRow(), 2).text()) != "0" else 
            [
                # Registrar moto
                db_connection.editarRegistroPC(
                    str(self.tabla_PCAgregados.item(self.tabla_PCAgregados.currentRow(), 0).text()),
                    str(self.tabla_PCAgregados.item(self.tabla_PCAgregados.currentRow(), 1).text()),
                ),
                # Actualizar la tabla
            ],self.actualizarTablaPCAgregados()
        ])
        
        boton_eliminar = QPushButton('ELIMINAR')
        boton_eliminar.setStyleSheet("color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;")
        layout_PC.addWidget(boton_eliminar, 7, 2, 1, 2,
                                alignment=Qt.AlignCenter| Qt.AlignHCenter)
        boton_eliminar.clicked.connect(lambda: [
            # Validaciones
            QMessageBox.warning(None, "Advertencia", "No hay registros seleccionados.") 
            if not self.tabla_PCAgregados.selectedItems() else 
            QMessageBox.warning(None, "Advertencia", "Este pc tiene casilleros asociados.") 
            if str(self.tabla_PCAgregados.item(self.tabla_PCAgregados.currentRow(), 2).text()) != "0" else 
            [
                # Registrar moto
                db_connection.eliminarPc(
                    str(self.tabla_PCAgregados.item(self.tabla_PCAgregados.currentRow(), 0).text()),
                ),
                # Actualizar la tabla
            ],self.actualizarTablaPCAgregados()
        ])
        # Crear el título y añadirlo a la sección izquierda
        titulo_PcActual= QLabel('PC ACTUAL')
        titulo_PcActual.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_PC.addWidget(titulo_PcActual, 8, 0, 1, 1, alignment=Qt.AlignCenter| Qt.AlignLeft)
        textbox_PCActual = QLineEdit()
        textbox_PCActual.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_PCActual.setFixedWidth(50)
        textbox_PCActual.setReadOnly(True)
        textbox_PCActual.setText(leer_archivo('config','PcActual.txt'))
        
        layout_PC.addWidget(textbox_PCActual, 8, 1, 1, 1, alignment=Qt.AlignCenter| Qt.AlignRight)
        #Parte derecha de la Tabla 
        titulo_ID= QLabel('ID')
        titulo_ID.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_PC.addWidget(titulo_ID, 3, 4, 1, 3, alignment=Qt.AlignCenter | Qt.AlignHCenter)
        textbox_ID = QLineEdit()
        textbox_ID.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        textbox_ID.setValidator(QIntValidator())
        layout_PC.addWidget(textbox_ID, 4, 4, 1, 3, alignment=Qt.AlignCenter | Qt.AlignTop)
        
        titulo_Descripcion= QLabel('DESCRIPCION')
        titulo_Descripcion.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_PC.addWidget(titulo_Descripcion,5, 4, 1, 3, alignment=Qt.AlignCenter | Qt.AlignHCenter)

        textbox_Descripcion = QLineEdit()
        textbox_Descripcion.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        layout_PC.addWidget(textbox_Descripcion, 6, 4, 1, 3, alignment=Qt.AlignCenter | Qt.AlignTop)

        boton_Guardar = QPushButton('Guardar')
        boton_Guardar.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 20px;")
        layout_PC.addWidget(boton_Guardar, 7, 4, 1, 3,
                                alignment=Qt.AlignHCenter| Qt.AlignCenter)
        boton_Guardar.clicked.connect(lambda: [
            db_connection.registrarPC(
            textbox_ID.text(),
            textbox_Descripcion.text()
        ),
        textbox_ID.clear(),
        textbox_Descripcion.clear(),
        self.actualizarComboboxpcs(),
        self.actualizarTablaPCAgregados()
    ])
        #Cambiar Pc
        titulo_CambiarPC= QLabel('CAMBIAR PC\nACTUAL')
        titulo_CambiarPC.setAlignment(Qt.AlignCenter)
        titulo_CambiarPC.setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_PC.addWidget(titulo_CambiarPC,8, 2, 1, 3, alignment=Qt.AlignCenter | Qt.AlignRight)

        self.combobox_pc = QComboBox()
        self.combobox_pc.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 30px;")
        layout_PC.addWidget(self.combobox_pc,8,5, 1, 1, alignment=Qt.AlignCenter|Qt.AlignHCenter)
        self.actualizarComboboxpcs()
        boton_Cambiar = QPushButton('CAMBIAR')
        boton_Cambiar.setStyleSheet("color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 20px;")
        layout_PC.addWidget(boton_Cambiar, 8, 6, 1, 1,
                                alignment=Qt.AlignHCenter| Qt.AlignCenter)
        #Se guarda la edición
        boton_Cambiar.clicked.connect(lambda: [
        escribir_archivo('config','PcActual.txt', self.combobox_pc.currentText()),
        self.actualizarComboboxpcs(),
        textbox_PCActual.setText(leer_archivo('config','PcActual.txt'))
    ])
        #Fila-Tamaño
        layout_PC.setRowStretch(0, 0)
        layout_PC.setRowStretch(1, 1)
        layout_PC.setRowStretch(2, 1)
        layout_PC.setRowStretch(3, 1)
        layout_PC.setRowStretch(4, 1)
        layout_PC.setRowStretch(5, 1)
        layout_PC.setRowStretch(6, 1)
        layout_PC.setRowStretch(7, 1)
        layout_PC.setRowStretch(8, 1)
        #Se agrega el layout a la pagina
        page_PC.setLayout(layout_PC)
        #se agrega la pagina al stack
        self.stacked_widgetConfiguracion.addWidget(page_PC)
    def actualizarTextboxesSuscripcion (self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        ultimoPago = db_connection.consultarUltimaSuscripcion()
        fechaActual = datetime.now().date()  # Convertir a objeto date
        
        if ultimoPago:
            # Asegurarse de que ultimoPago sea un objeto date
            if isinstance(ultimoPago, str):
                ultimoPago = datetime.strptime(ultimoPago, '%Y-%m-%d').date()
            
            dias_restantes = 30 - (fechaActual - ultimoPago).days  # Calcular la diferencia en días
            self.textboxDiasRestantesSuscripcion.setText(str(dias_restantes))
            
            if dias_restantes > 0:
                self.textboxEstadoActualSuscripcion.setText("ACTIVA")
            else:
                self.textboxEstadoActualSuscripcion.setText("INACTIVA")

    def verificarCodigoMensualidad(self, textoCodigo):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        fecha_str = datetime.now().strftime('%Y-%m-%d')
        fecha_actual = datetime.strptime(fecha_str, "%Y-%m-%d")
        dia = fecha_actual.day
        codigo = generarCodigoEncriptado("parqueaderola18", str(fecha_str), int(dia))  # Se genera un código a partir de una palabra clave, la fecha y un numero de iteraciones, que variará en función del día
        if textoCodigo == codigo:
            print("Suscripción Activada")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Su suscripcón ha sido renovada.")
            msg.setWindowTitle("Renovación correcta")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            db_connection.registrarSuscripcion()
            self.actualizarTextboxesSuscripcion()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("El código es erroneo, porfavor verifíquelo.")
            msg.setWindowTitle("Error en el código")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            print("Código erróneo")

    def pantallaSuscripcion(self):
         #Pagina de Suscripcion
        page_Suscripcion = QWidget()
        #Layout de la Pagina de Suscripcion
        layout_Suscripcion = QGridLayout()
        #------------------------------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_Suscripcion= QLabel('SUSCRIPCIÓN')
        titulo_Suscripcion.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_Suscripcion.addWidget(titulo_Suscripcion, 0, 0, 1, 7, alignment=Qt.AlignTop | Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_Suscripcion.addWidget(linea_horizontal1, 1, 0, 1, 7)
        #Titulo
        titulo_Codigo = QLabel('CÓDIGO')
        titulo_Codigo .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_Suscripcion.addWidget(titulo_Codigo  , 2, 0, 1, 7, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        textbox_Codigo = QLineEdit()
        textbox_Codigo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        layout_Suscripcion.addWidget(textbox_Codigo,3, 0, 2, 7, alignment=Qt.AlignHCenter |Qt.AlignTop)
        #Boton Validar
        boton_validar = QPushButton('VALIDAR')
        boton_validar.setStyleSheet("color: White; background-color: #222125; font-size: 35px; border-radius: 15px; padding: 10px 20px;")
        layout_Suscripcion.addWidget(boton_validar,4, 0, 1, 7,alignment=Qt.AlignHCenter |Qt.AlignTop)
         # Conectar el botón de imprimir a la función registrarMoto
        boton_validar.clicked.connect(lambda: [
            self.verificarCodigoMensualidad(
                textbox_Codigo.text()
        ),
            textbox_Codigo.clear()
        ])


        titulo_EstadoActual= QLabel('ESTADO ACTUAL')
        titulo_EstadoActual .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_Suscripcion.addWidget(titulo_EstadoActual  , 6, 3, 1, 1, alignment= Qt.AlignCenter |Qt.AlignCenter)

        self.textboxEstadoActualSuscripcion = QLineEdit()
        self.textboxEstadoActualSuscripcion.setStyleSheet("color: #89d631 ; margin: 0; padding: 0; font-size: 30px;")
        self.textboxEstadoActualSuscripcion.setReadOnly(True)
        layout_Suscripcion.addWidget(self.textboxEstadoActualSuscripcion, 6, 4, 1, 1, alignment=Qt.AlignCenter |Qt.AlignCenter)


        tituloDiasRestantesSuscripción = QLabel('DIAS RESTANTES')
        tituloDiasRestantesSuscripción .setStyleSheet("color: #FFFFFF;font-size: 30px; font-weight: bold;")
        layout_Suscripcion.addWidget(tituloDiasRestantesSuscripción  , 7, 3, 1, 1, alignment= Qt.AlignTop |Qt.AlignCenter)

        self.textboxDiasRestantesSuscripcion = QLineEdit()
        self.textboxDiasRestantesSuscripcion.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        self.textboxDiasRestantesSuscripcion.setReadOnly(True)
        layout_Suscripcion.addWidget(self.textboxDiasRestantesSuscripcion, 7, 4, 1, 1, alignment=Qt.AlignCenter|Qt.AlignTop)
        self.actualizarTextboxesSuscripcion() #Actualizar etxboxes
        #Fila-Tamaño
        layout_Suscripcion.setRowStretch(0, 0)
        layout_Suscripcion.setRowStretch(1, 1)
        layout_Suscripcion.setRowStretch(2, 1)
        layout_Suscripcion.setRowStretch(3, 1)
        layout_Suscripcion.setRowStretch(4, 1)
        layout_Suscripcion.setRowStretch(5, 1)
        layout_Suscripcion.setRowStretch(6, 1)
        layout_Suscripcion.setRowStretch(7, 1)
        layout_Suscripcion.setRowStretch(8, 1)

        #Se agrega el layout a la pagina
        page_Suscripcion.setLayout(layout_Suscripcion)
        #se agrega la pagina al stack
        self.stacked_widgetConfiguracion.addWidget(page_Suscripcion)
