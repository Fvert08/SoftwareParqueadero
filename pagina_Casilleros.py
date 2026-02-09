from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout,QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView
from PyQt5.QtCore import pyqtSignal
# base de datos
from DatabaseConnection import DatabaseConnection
from config import DB_CONFIG
from styles import LABELS, LINEAS, BOTONES, INPUTS, COMBOBOX, TABLAS, CHECKBOXES, CALENDARIOS, OTROS
class PaginaCasilleros(QWidget):
    senalActualizarTextboxesTicketsRegistrosMotos = pyqtSignal()
    senalActualizarComboboxPcs= pyqtSignal()
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()
    def actualizarTablaCasillero(self):
         # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        datosTablaCasillero= db_connection.cargarTableCasillero()
        self.tabla_registrosCasillero.setRowCount(len(datosTablaCasillero))
        for row_idx, registro in enumerate(datosTablaCasillero):
            item_id = QTableWidgetItem(str(registro['id']))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tabla_registrosCasillero.setItem(row_idx, 0, item_id)

            item_casillero = QTableWidgetItem(str(registro['Pc']))
            item_casillero.setTextAlignment(Qt.AlignCenter)
            self.tabla_registrosCasillero.setItem(row_idx, 1, item_casillero)

            item_pisicion = QTableWidgetItem(str(registro['Posicion']))
            item_pisicion.setTextAlignment(Qt.AlignCenter)
            self.tabla_registrosCasillero.setItem(row_idx, 2, item_pisicion)

            item_estado = QTableWidgetItem(str(registro['Estado']))
            item_estado.setTextAlignment(Qt.AlignCenter)
            self.tabla_registrosCasillero.setItem(row_idx, 3, item_estado)

            casillero_value = registro['id']
            
            Placa = db_connection.obtenerPlacaPorCasillero(casillero_value)

            # Si obtenerPlacaPorCasillero devuelve 0 → se muestra "0"
            # Si obtenerPlacaPorCasillero devuelve None → se muestra "" (cadena vacía)
            # Si obtenerPlacaPorCasillero devuelve una placa válida → se muestra la placa como string
            texto_placa = "0" if Placa == 0 else ("" if Placa is None else str(Placa))
            item_Placa = QTableWidgetItem(texto_placa)
            item_Placa.setTextAlignment(Qt.AlignCenter)
            self.tabla_registrosCasillero.setItem(row_idx, 4, item_Placa)


    def actualizarTablaCasilleroOrden(self):
         # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        datosTablaCasilleroOrden= db_connection.cargarTableCasilleroOrden()
        self.tablaOrdenDeLlenado.setRowCount(len(datosTablaCasilleroOrden))
        for row_idx, registro in enumerate(datosTablaCasilleroOrden):
            item_id = QTableWidgetItem(str(registro['Posicion']))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tablaOrdenDeLlenado.setItem(row_idx, 0, item_id)

            item_id = QTableWidgetItem(str(registro['id']))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tablaOrdenDeLlenado.setItem(row_idx, 1, item_id)

            item_casillero = QTableWidgetItem(str(registro['Estado']))
            item_casillero.setTextAlignment(Qt.AlignCenter)
            self.tablaOrdenDeLlenado.setItem(row_idx, 2, item_casillero)

            item_pisicion = QTableWidgetItem(str(registro['Pc']))
            item_pisicion.setTextAlignment(Qt.AlignCenter)
            self.tablaOrdenDeLlenado.setItem(row_idx, 3, item_pisicion)
    def actualizarTablasCasilleros (self):
        self.actualizarTablaCasillero()
        self.actualizarTablaCasilleroOrden()
        self.senalActualizarTextboxesTicketsRegistrosMotos.emit()
    def actualizarComboboxpcs (self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        ids = db_connection.obtenerIdsRegPc()
        self.combobox_pcRegistro.clear()
        self.combobox_pcCambiar.clear()
        self.combobox_pcCambiar.addItems(map(str, ids))
        self.combobox_pcRegistro.addItems(map(str, ids))

    def initUI(self):
         # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Crear el widget de la página de registros
        page_casilleros = QWidget()

        # Crear un layout para organizar los elementos en la página
        layout_tickets = QGridLayout()

        titulo_casilleros = QLabel('GESTIONAR CASILLEROS')
        titulo_casilleros.setStyleSheet(LABELS['casilleros_titulo_casilleros'])
        layout_tickets.addWidget(titulo_casilleros, 0, 0, 1, 10, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINEAS['casilleros_linea_horizontal1'])
        layout_tickets.addWidget(linea_horizontal1, 1, 0, 1, 10)

        titulo_tablacasilleros = QLabel('CASILLEROS')
        titulo_tablacasilleros.setStyleSheet(LABELS['casilleros_titulo_tablacasilleros'])
        layout_tickets.addWidget(titulo_tablacasilleros, 2, 0, 1, 4, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        
        titulo_agregarCasillero = QLabel('AGREGAR CASILLERO')
        titulo_agregarCasillero.setStyleSheet(LABELS['casilleros_titulo_agregar_casillero'])
        layout_tickets.addWidget(titulo_agregarCasillero, 8, 0, 1, 4, alignment= Qt.AlignTop|Qt.AlignHCenter)

        titulo_numero = QLabel('NUMERO')
        titulo_numero .setStyleSheet(LABELS['casilleros_titulo_numero'])
        layout_tickets.addWidget(titulo_numero , 8, 0, 1, 1, alignment= Qt.AlignBottom |Qt.AlignHCenter)

        textbox_numero = QLineEdit()
        textbox_numero.setStyleSheet(INPUTS['casilleros_textbox_numero'])
        textbox_numero.setValidator(QIntValidator())
        layout_tickets.addWidget(textbox_numero, 8, 1, 1, 1, alignment= Qt.AlignBottom |Qt.AlignHCenter)

        titulo_pc = QLabel('PC')
        titulo_pc.setStyleSheet(LABELS['casilleros_titulo_pc'])
        layout_tickets.addWidget(titulo_pc , 8, 2, 1, 1, alignment= Qt.AlignBottom |Qt.AlignHCenter)

        self.combobox_pcRegistro = QComboBox()
        self.combobox_pcRegistro.setStyleSheet(COMBOBOX['casilleros_combobox_pc_registro'])
        layout_tickets.addWidget(self.combobox_pcRegistro,8, 3, 1, 1, alignment= Qt.AlignBottom |Qt.AlignHCenter)

        titulo_estado = QLabel('ESTADO')
        titulo_estado .setStyleSheet(LABELS['casilleros_titulo_estado'])
        layout_tickets.addWidget(titulo_estado , 9, 0, 1, 1, alignment= Qt.AlignCenter|Qt.AlignHCenter)

        combobox_Estado = QComboBox()
        combobox_Estado.addItems(['DISPONIBLE','OCUPADO'])
        combobox_Estado.setStyleSheet(COMBOBOX['casilleros_combobox_estado'])
        layout_tickets.addWidget(combobox_Estado,9, 1, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)

        boton_agregar = QPushButton('AGREGAR')
        boton_agregar.setStyleSheet(BOTONES['casilleros_boton_agregar'])
        layout_tickets.addWidget(boton_agregar,9, 2, 1, 1, alignment= Qt.AlignCenter |Qt.AlignHCenter)
        boton_agregar.clicked.connect(lambda: [
            db_connection.registrarCasillero(
            textbox_numero.text(),
            self.combobox_pcRegistro.currentText(),
            combobox_Estado.currentText()
        ),
        self.combobox_pcRegistro.setCurrentIndex(0),
        combobox_Estado.setCurrentIndex(0),
        textbox_numero.clear(),
        self.actualizarTablaCasillero(),
        self.actualizarTablaCasilleroOrden(),
        self.actualizarComboboxpcs()
    ])
        self.tabla_registrosCasillero = QTableWidget(self)
        self.tabla_registrosCasillero.setColumnCount(5)  # Definir el número de columnas
        self.tabla_registrosCasillero.verticalHeader().setVisible(False)
        self.tabla_registrosCasillero.setHorizontalHeaderLabels(
            ['NUMERO', 'PC', 'Posicion', 'Estado','Placa'])
        self.tabla_registrosCasillero.setStyleSheet(TABLAS['casilleros_tabla_registros_casillero'])
        header = self.tabla_registrosCasillero.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        #se configuran las propiedades de latabla, para que se seleccione toda la fila y no se permita editar
        self.tabla_registrosCasillero.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_registrosCasillero.setSelectionBehavior(QAbstractItemView.SelectRows)

        #---- aqui se carga la tabla
        self.actualizarTablaCasillero()
        layout_tickets.addWidget(self.tabla_registrosCasillero, 3, 0, 5, 4)

        boton_desocupar = QPushButton('DESOCUPAR')
        boton_desocupar.setStyleSheet(BOTONES['casilleros_boton_desocupar'])
        layout_tickets.addWidget(boton_desocupar, 3, 4, 1, 2,
                                alignment=Qt.AlignCenter| Qt.AlignHCenter)
        # Conectar el botón de imprimir a la función registrarMoto
        boton_desocupar.clicked.connect(lambda: [
             self.tabla_registrosCasillero.selectedItems() and db_connection.cambiarEstadoCasillero(
            self.tabla_registrosCasillero.item(self.tabla_registrosCasillero.currentRow(), 0).text(),
            self.tabla_registrosCasillero.item(self.tabla_registrosCasillero.currentRow(), 3).text(),
        ),
        self.actualizarTablasCasilleros()
    ])

        
        boton_eliminar = QPushButton('ELIMINAR')
        boton_eliminar.setStyleSheet(BOTONES['casilleros_boton_eliminar'])
        layout_tickets.addWidget(boton_eliminar, 4, 4, 1, 2,
                                alignment=Qt.AlignCenter| Qt.AlignHCenter)
        #---
        boton_eliminar.clicked.connect(lambda: [
            self.tabla_registrosCasillero.selectedItems() and db_connection.eliminarCasillero(
            self.tabla_registrosCasillero.item(self.tabla_registrosCasillero.currentRow(), 0).text(),
            int(self.tabla_registrosCasillero.item(self.tabla_registrosCasillero.currentRow(), 2).text()),
            self.tabla_registrosCasillero.item(self.tabla_registrosCasillero.currentRow(), 3).text()
        ),
        self.actualizarTablaCasillero(),
        self.actualizarTablaCasilleroOrden()
    ])
        #---
        titulo_cambiarPc = QLabel('CAMBIAR PC')
        titulo_cambiarPc .setStyleSheet(LABELS['casilleros_titulo_cambiar_pc'])
        layout_tickets.addWidget(titulo_cambiarPc, 5, 4, 1, 2,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        
        titulo_pcCambiar = QLabel('PC')
        titulo_pcCambiar.setStyleSheet(LABELS['casilleros_titulo_pc_cambiar'])
        layout_tickets.addWidget(titulo_pcCambiar , 6, 4, 1, 1, alignment= Qt.AlignRight|Qt.AlignTop)

        self.combobox_pcCambiar = QComboBox()
        self.combobox_pcCambiar.setFixedWidth(50)
        self.combobox_pcCambiar.setStyleSheet(COMBOBOX['casilleros_combobox_pc_cambiar'])
        layout_tickets.addWidget(self.combobox_pcCambiar,6, 5, 1, 1, alignment=Qt.AlignLeft |Qt.AlignTop)
        self.actualizarComboboxpcs()
        boton_guardarPc = QPushButton('GUARDAR')
        boton_guardarPc.setStyleSheet(BOTONES['casilleros_boton_guardar_pc'])
        layout_tickets.addWidget(boton_guardarPc,7, 4, 1, 2,
                                alignment=Qt.AlignTop| Qt.AlignHCenter)
        #Se guarda la edición
        boton_guardarPc.clicked.connect(lambda: [
            self.tabla_registrosCasillero.currentRow() != -1 and db_connection.cambiarPcCasillero(
            self.tabla_registrosCasillero.item(self.tabla_registrosCasillero.currentRow(), 0).text(),
            self.combobox_pcCambiar.currentText(),
        ),
        self.actualizarTablasCasilleros(),
        self.actualizarComboboxpcs()
    ])


        titulo_tablaOrdenDeLlegada = QLabel('ORDEN DE LLENADO')
        titulo_tablaOrdenDeLlegada.setStyleSheet(LABELS['casilleros_titulo_tabla_orden_de_llegada'])
        layout_tickets.addWidget(titulo_tablaOrdenDeLlegada, 2, 6, 1, 3, alignment= Qt.AlignCenter |Qt.AlignTop)
        self.tablaOrdenDeLlenado = QTableWidget(self)
        self.tablaOrdenDeLlenado.setColumnCount(4)  # Definir el número de columnas
        self.tablaOrdenDeLlenado.verticalHeader().setVisible(False)
        self.tablaOrdenDeLlenado.setHorizontalHeaderLabels(
            ['POSICION','NUMERO', 'ESTADO', 'PC'])
        self.tablaOrdenDeLlenado.setStyleSheet(TABLAS['casilleros_tabla_orden_de_llenado'])
        header = self.tablaOrdenDeLlenado.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
         #se configuran las propiedades de latabla, para que se seleccione toda la fila y no se permita editar
        self.tablaOrdenDeLlenado.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablaOrdenDeLlenado.setSelectionBehavior(QAbstractItemView.SelectRows)
        #---- aqui se carga la tabla
        self.actualizarTablaCasilleroOrden()
        layout_tickets.addWidget(self.tablaOrdenDeLlenado, 3, 6, 5, 3)

        boton_subir = QPushButton('SUBIR')
        boton_subir.setStyleSheet(BOTONES['casilleros_boton_subir'])
        layout_tickets.addWidget(boton_subir, 3, 9, 2, 1,
                                alignment=Qt.AlignTop| Qt.AlignHCenter)
        boton_subir.clicked.connect(lambda: [
            self.tablaOrdenDeLlenado.selectedItems() and db_connection.subirPosicionCasillero(
            int(self.tablaOrdenDeLlenado.item(self.tablaOrdenDeLlenado.currentRow(), 0).text())
        ),
        self.actualizarTablasCasilleros(),
          self.tablaOrdenDeLlenado.selectedItems() and self.tablaOrdenDeLlenado.setCurrentCell(self.tablaOrdenDeLlenado.currentRow() - 1, 0)
        
        ])

        boton_bajar = QPushButton('BAJAR')
        boton_bajar.setStyleSheet(BOTONES['casilleros_boton_bajar'])
        layout_tickets.addWidget(boton_bajar, 3, 9, 2, 1,
                                alignment=Qt.AlignCenter| Qt.AlignHCenter)
        boton_bajar.clicked.connect(lambda: [
             self.tablaOrdenDeLlenado.selectedItems() and db_connection.bajarPosicionCasillero(
            int(self.tablaOrdenDeLlenado.item(self.tablaOrdenDeLlenado.currentRow(), 0).text())
        ),
        self.actualizarTablasCasilleros(),
        self.tablaOrdenDeLlenado.selectedItems() and self.tablaOrdenDeLlenado.setCurrentCell(self.tablaOrdenDeLlenado.currentRow() + 1, 0)
        ])
  
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
        layout_tickets.setRowStretch(9, 1)
        self.stacked_widget.addWidget(page_casilleros)
    