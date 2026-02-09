from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame,QStackedWidget, QComboBox,QLineEdit,QGridLayout,QCheckBox,QTableWidget,QHBoxLayout,QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
from datetime import datetime, date
from DatabaseConnection import DatabaseConnection
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from config import DB_CONFIG
from generarTickets.TicketIngresoMoto import generarTicketIngresoMoto
from generarTickets.TicketIngresoMensualidad import generarTicketIngresoMensualidad
from generarTickets.TicketIngresoFijo import generarTicketIngresoFijo
from generarTickets.TicketRenovarMensualidad import generarTicketRenovarMensualidad
from styles import LABELS, LINEAS, BOTONES, INPUTS, COMBOBOX, TABLAS, CHECKBOXES, CALENDARIOS, OTROS
class PaginaRegistros(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def actualizarTablaMensualidades(self):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        if self.combobox_FiltrarRegistrosMensualidad.currentText() !="Todo":
            datosTablaMensualides= db_connection.cargarTableRegistrosMensualidadFiltrada(self.combobox_FiltrarRegistrosMensualidad.currentText(),self.textbox_FiltrarRegistrosMensualidad.text()) 
        else :
            datosTablaMensualides = db_connection.cargarTableMensualidades()
        
        self.tabla_Mensualidades.setRowCount(len(datosTablaMensualides))
        for row_idx, registro in enumerate(datosTablaMensualides):
            item_id = QTableWidgetItem(str(registro['id']))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tabla_Mensualidades.setItem(row_idx, 0, item_id)

            item_placa = QTableWidgetItem(registro['Placa'])
            item_placa.setTextAlignment(Qt.AlignCenter)
            self.tabla_Mensualidades.setItem(row_idx, 1, item_placa)

            item_nombre = QTableWidgetItem(registro['Nombre'])
            item_nombre.setTextAlignment(Qt.AlignCenter)
            self.tabla_Mensualidades.setItem(row_idx, 2, item_nombre)

            item_telefono = QTableWidgetItem(registro['Telefono'])
            item_telefono.setTextAlignment(Qt.AlignCenter)
            self.tabla_Mensualidades.setItem(row_idx, 3, item_telefono)

            item_fecha_ingreso = QTableWidgetItem(registro['fechaIngreso'].strftime('%Y-%m-%d') if isinstance(registro['fechaIngreso'], (datetime, date)) else str(registro['fechaIngreso']))
            item_fecha_ingreso.setTextAlignment(Qt.AlignCenter)
            self.tabla_Mensualidades.setItem(row_idx, 4, item_fecha_ingreso)

            item_hora_ingreso = QTableWidgetItem(str(registro.get('horaIngreso')))
            item_hora_ingreso.setTextAlignment(Qt.AlignCenter)
            self.tabla_Mensualidades.setItem(row_idx, 5, item_hora_ingreso)

            item_fechaUltimoPago = QTableWidgetItem(registro['fechaUltimoPago'].strftime('%Y-%m-%d') if isinstance(registro['fechaIngreso'], (datetime, date)) else str(registro['fechaIngreso']))
            item_fechaUltimoPago.setTextAlignment(Qt.AlignCenter)
            self.tabla_Mensualidades.setItem(row_idx, 6, item_fechaUltimoPago)

            item_horaUltimoPago = QTableWidgetItem(str(registro.get('horaUltimoPago')))
            item_horaUltimoPago.setTextAlignment(Qt.AlignCenter)
            self.tabla_Mensualidades.setItem(row_idx, 7, item_horaUltimoPago)

            item_fechaRenovacion = QTableWidgetItem(str(registro.get('fechaRenovacion')))
            item_fechaRenovacion.setTextAlignment(Qt.AlignCenter)
            self.tabla_Mensualidades.setItem(row_idx, 8, item_fechaRenovacion)
  

    def actualizarTablaRegistroMotos(self):
         # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Abre la conexión a la base de datos
        if self.combobox_FiltroRegistroMoto.currentText() !="Todo":
            datosTablaRegistroMotos= db_connection.cargarTableRegistrosMotosFiltrada(self.combobox_FiltroRegistroMoto.currentText(),self.textbox_FiltroRegistroMoto.text()) 
        else :
            datosTablaRegistroMotos= db_connection.cargarTableRegistrosMotos()
        self.tablaRegistrosMotos.setRowCount(len(datosTablaRegistroMotos))
        for row_idx, registro in enumerate(datosTablaRegistroMotos):
            item_id = QTableWidgetItem(str(registro['id']))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 0, item_id)

            item_casillero = QTableWidgetItem(str(registro['Casillero']))
            item_casillero.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 1, item_casillero)

            item_placa = QTableWidgetItem(registro['Placa'])
            item_placa.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 2, item_placa)

            item_cascos = QTableWidgetItem(str(registro['Cascos']))
            item_cascos.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 3, item_cascos)

            item_tipo = QTableWidgetItem(registro['Tipo'])
            item_tipo.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 4, item_tipo)

            item_fecha_ingreso = QTableWidgetItem(registro['fechaIngreso'].strftime('%Y-%m-%d') if isinstance(registro['fechaIngreso'], (datetime, date)) else str(registro['fechaIngreso']))
            item_fecha_ingreso.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 5, item_fecha_ingreso)

            item_hora_ingreso = QTableWidgetItem(str(registro.get('horaIngreso', '')))
            item_hora_ingreso.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 6, item_hora_ingreso)

            # Fecha de salida: Si es None, se pone ""
            fecha_salida = registro.get('fechaSalida')
            fecha_salida_str = fecha_salida.strftime('%Y-%m-%d') if isinstance(fecha_salida, (datetime, date)) else (str(fecha_salida) if fecha_salida else "")
            item_fecha_salida = QTableWidgetItem(fecha_salida_str)
            item_fecha_salida.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 7, item_fecha_salida)

            # Hora de salida: Si es None, se pone ""
            hora_salida = registro.get('horaSalida', "")
            item_hora_salida = QTableWidgetItem(str(hora_salida) if hora_salida else "")
            item_hora_salida.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 8, item_hora_salida)

            # Total: Si es None, se pone ""
            total = registro.get('Total', "")
            item_total = QTableWidgetItem(str(total) if total else "")
            item_total.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 9, item_total)
        # Bloquear columnas que no se pueden editar
        for row in range(self.tablaRegistrosMotos.rowCount()):
            for col in [0, 1, 5, 6, 7, 8, 9]:  # Columnas a bloquear
                item = self.tablaRegistrosMotos.item(row, col)
                if item:  
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)


    def actualizarTablaFijos(self):
         # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        # Abre la conexión a la base de datos
        if self.combobox_filtroRegistroFijos.currentText() !="Todo":
            datosTablaRegistroFijos= db_connection.cargarTableRegistrosFijosFiltrada(self.combobox_filtroRegistroFijos.currentText(),self.textbox_FiltroRegistroFijo.text()) 
        else :
            datosTablaRegistroFijos= db_connection.cargarTableRegistrosFijos()
        
        self.tablaRegistrosFijos.setRowCount(len(datosTablaRegistroFijos))

        for row_idx, registro in enumerate(datosTablaRegistroFijos):
            item_id = QTableWidgetItem(str(registro['id']))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 0, item_id)

            item_casillero = QTableWidgetItem(str(registro['Tipo']))
            item_casillero.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 1, item_casillero)

            item_placa = QTableWidgetItem(registro['Nota'])
            item_placa.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 2, item_placa)

            item_fecha_ingreso = QTableWidgetItem(registro['fechaIngreso'].strftime('%Y-%m-%d') if isinstance(registro['fechaIngreso'], (datetime, date)) else str(registro['fechaIngreso']))
            item_fecha_ingreso.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 3, item_fecha_ingreso)

            item_hora_ingreso = QTableWidgetItem(str(registro.get('horaIngreso', '')))
            item_hora_ingreso.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 4, item_hora_ingreso)

            # Fecha de salida: Si es None, se pone ""
            fecha_salida = registro.get('fechaSalida')
            fecha_salida_str = fecha_salida.strftime('%Y-%m-%d') if isinstance(fecha_salida, (datetime, date)) else (str(fecha_salida) if fecha_salida else "")
            item_fecha_salida = QTableWidgetItem(fecha_salida_str)
            item_fecha_salida.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 5, item_fecha_salida)

            # Hora de salida: Si es None, se pone ""
            hora_salida = registro.get('horaSalida', "")
            item_hora_salida = QTableWidgetItem(str(hora_salida) if hora_salida else "")
            item_hora_salida.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 6, item_hora_salida)

            item_total = QTableWidgetItem(str(registro.get('Valor', '')))
            item_total.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 7, item_total)
        # Bloquear columnas que no se pueden editar
        for row in range(self.tablaRegistrosMotos.rowCount()):
            for col in [0, 1, 3, 4, 5, 6, 7]:  # Columnas a bloquear
                item = self.tablaRegistrosFijos.item(row, col)
                if item:  
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)


    def initUI(self):
       # Crear el widget de la página de registros
        page_registros = QWidget()
        #Pagina del menú
        page_registrosmenu = QWidget()
        # -----Stack para agregar todas las pantallas de tickets
        self.stacked_widgetregistros = QStackedWidget()

        #--------#layouts (Izquierdo, derecho y principal)
        #layout Menu derecho donde se agregan todos los botones
        layout_registros = QGridLayout()
        
        #layout principal box horizontal
        main_layoutregistros = QHBoxLayout()
         #Se llaman las pantallas para cargarlas en el stack
        self.pantallaTablaRegistros()
        self.pantallaTablaFijos()
        self.pantallaTablaMensualidades()
        self.pantallaTablaResumen()
        #------------------------Menu lateral---------------------------
        # Crear la línea vertical de 1 pixel y añadirla a la cuadrícula
        linea_vertical = QFrame()
        linea_vertical.setFrameShape(QFrame.VLine)
        linea_vertical.setLineWidth(1)
        linea_vertical.setStyleSheet(LINEAS['registros_linea_vertical'])
        layout_registros.addWidget(linea_vertical, 0, 0, 9, 1)  # Cambiado de 8 a 9 filas
        
        # Crear la sección derecha con el título "Menú"
        titulo_menu = QLabel('MENÚ')
        titulo_menu.setStyleSheet(LABELS['registros_titulo_menu'])
        layout_registros.addWidget(titulo_menu, 0, 1, 1, 1, alignment= Qt.AlignCenter)

        linea_horizontal2 = QFrame()
        linea_horizontal2.setFrameShape(QFrame.HLine)
        linea_horizontal2.setLineWidth(1)
        linea_horizontal2.setStyleSheet(LINEAS['registros_linea_horizontal2'])
        layout_registros.addWidget(linea_horizontal2, 1, 1, 1, 1)
        
        # Crea un boton para cambiar a Registros
        boton_Registros= QPushButton("REGISTROS")
        boton_Registros.setStyleSheet(BOTONES['registros_boton_registros'])
        layout_registros.addWidget(boton_Registros, 2, 1, 1, 1)
        boton_Registros.setCheckable(True)
        boton_Registros.setChecked(True)
        boton_Registros.pressed.connect(lambda: self.stacked_widgetregistros.setCurrentIndex(0))
        
        # Crea un boton para cambiar a Fijos
        boton_Fijos = QPushButton("FIJOS")
        boton_Fijos.setStyleSheet(BOTONES['registros_boton_fijos'])
        layout_registros.addWidget(boton_Fijos, 3, 1, 1, 1)
        boton_Fijos.setCheckable(True)
        boton_Fijos.pressed.connect(lambda: self.stacked_widgetregistros.setCurrentIndex(1))
      
        # Crea un boton para cambiar a las Mensualidades
        boton_Mensualidades = QPushButton("MENSUALIDADES")
        boton_Mensualidades.setStyleSheet(BOTONES['registros_boton_mensualidades'])
        layout_registros.addWidget(boton_Mensualidades, 4, 1, 1, 1)
        boton_Mensualidades.setCheckable(True)
        boton_Mensualidades.pressed.connect(lambda: self.stacked_widgetregistros.setCurrentIndex(2))

       # Crea un botón para Resumen en la parte inferior
        boton_Resumen = QPushButton("RESUMEN")
        boton_Resumen.setStyleSheet(BOTONES['registros_boton_resumen'])
        layout_registros.addWidget(boton_Resumen, 8, 1, 1, 1)  # Posición 8 (parte inferior)
        boton_Resumen.setCheckable(True)
        boton_Resumen.pressed.connect(lambda:self.stacked_widgetregistros.setCurrentIndex(3))

        # Configuración del stretch para mantener los botones superiores juntos y el botón Resumen abajo
        layout_registros.setRowStretch(0, 0)  # Título
        layout_registros.setRowStretch(1, 0)  # Línea horizontal
        layout_registros.setRowStretch(2, 0)  # Botón Registros
        layout_registros.setRowStretch(3, 0)  # Botón Fijos
        layout_registros.setRowStretch(4, 0)  # Botón Mensualidades
        layout_registros.setRowStretch(5, 1)  # Espacio expandible
        layout_registros.setRowStretch(6, 0)  # 
        layout_registros.setRowStretch(7, 0)  # 
        layout_registros.setRowStretch(8, 0)  # Botón Resumen
        
        #Se agrega el layout a la pagina
        page_registrosmenu.setLayout(layout_registros)
        #Se agrega el stack al layout principal
        main_layoutregistros.addWidget(self.stacked_widgetregistros)
        #se agrega el menú al layout principal
        main_layoutregistros.addWidget(page_registrosmenu)
        #se agrega el layout principal a la pagina principal
        page_registros.setLayout(main_layoutregistros)
        #se llama la primera posición del stack
        self.stacked_widgetregistros.setCurrentIndex(0)
        #Se agrega al stack
        self.stacked_widget.addWidget(page_registros)

    def pantallaTablaRegistros(self):
         # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)

        # Abre la conexión a la base de datos
        #Pagina de Usuarios
        page_TablaRegistros = QWidget()
        #Layout de la Pagina de Usuarios
        layout_TablaRegistros = QGridLayout()
        #------------------------------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_Registros = QLabel('REGISTROS')
        titulo_Registros.setStyleSheet(LABELS['registros_titulo_registros'])
        layout_TablaRegistros.addWidget(titulo_Registros, 0, 0, 1, 9,alignment=Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINEAS['registros_linea_horizontal1'])
        layout_TablaRegistros.addWidget(linea_horizontal1, 1, 0, 1, 9)
         # Crear la tabla de registros
        self.tablaRegistrosMotos = QTableWidget(self)
        self.tablaRegistrosMotos.setColumnCount(10)  # Definir el número de columnas
        self.tablaRegistrosMotos.verticalHeader().setVisible(False)
        self.tablaRegistrosMotos.setHorizontalHeaderLabels(
            ['ID', 'CASILLERO', 'PLACA', 'CASCOS', 'TIPO', 'F.INGRESO', 'H.INGRESO', 'F.SALIDA','H.SALIDA', 'TOTAL'])
        self.tablaRegistrosMotos.setStyleSheet(TABLAS['registros_tabla_registros_motos'])
        #seleccionar toda la fila
        self.tablaRegistrosMotos.setSelectionBehavior(QAbstractItemView.SelectRows)
        #Configurar cabecera
        header = self.tablaRegistrosMotos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        layout_TablaRegistros.addWidget(self.tablaRegistrosMotos, 2, 0, 6, 9)
        #Botones del filtro
        self.combobox_FiltroRegistroMoto = QComboBox()
        self.combobox_FiltroRegistroMoto.addItems(['Todo', "ID" ,'Casillero', 'Placa', 'Tipo'])
        self.combobox_FiltroRegistroMoto.setStyleSheet(COMBOBOX['registros_combobox_filtro_registro_moto'])
        layout_TablaRegistros.addWidget(self.combobox_FiltroRegistroMoto, 8, 0, 1, 1)
        
        self.textbox_FiltroRegistroMoto = QLineEdit()
        self.textbox_FiltroRegistroMoto.setStyleSheet(INPUTS['registros_textbox_filtro_registro_moto'])
        layout_TablaRegistros.addWidget(self.textbox_FiltroRegistroMoto , 8, 1, 1, 1)
        # Rellenar la tabla dependiendo de lo seleccionado en el combo box
        self.actualizarTablaRegistroMotos()
        #Boton Buscar 
        boton_Buscar = QPushButton('BUSCAR')
        boton_Buscar .setStyleSheet(BOTONES['registros_boton_buscar'])
        layout_TablaRegistros.addWidget(boton_Buscar , 8, 2, 1, 1)
        boton_Buscar.clicked.connect(lambda: [
            self.actualizarTablaRegistroMotos()
            ])
        #Boton Reimprimir Registro
        boton_ReimprimirRegistro= QPushButton('REIMPRIMIR INGRESO')
        boton_ReimprimirRegistro .setStyleSheet(BOTONES['registros_boton_reimprimir_registro'])
        layout_TablaRegistros.addWidget(boton_ReimprimirRegistro , 8, 5, 1, 1)
        boton_ReimprimirRegistro.clicked.connect(lambda: [
            self.tablaRegistrosMotos.selectedItems() and generarTicketIngresoMoto(int(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 0).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 4).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 2).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 3).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 1).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 5).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 6).text()),
        )])
        #Boton Eliminar Registro
        boton_EliminarRegistro= QPushButton('ELIMINAR REGISTRO')
        boton_EliminarRegistro .setStyleSheet(BOTONES['registros_boton_eliminar_registro'])
        layout_TablaRegistros.addWidget(boton_EliminarRegistro , 8, 6, 1, 1)
        boton_EliminarRegistro.clicked.connect(lambda: [
            self.tablaRegistrosMotos.selectedItems() and db_connection.eliminarRegistroMoto(
                                int(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 0).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 7).text()),
        ),
        self.actualizarTablaRegistroMotos()])
        #Boton Guardar Edicion 
        boton_GuardarEdicion= QPushButton('GUARDAR EDICIÓN')
        boton_GuardarEdicion .setStyleSheet(BOTONES['registros_boton_guardar_edicion'])
        layout_TablaRegistros.addWidget(boton_GuardarEdicion , 8, 7, 1, 1)
        boton_GuardarEdicion.clicked.connect(lambda: [
             self.tablaRegistrosMotos.selectedItems() and db_connection.editarRegistroMoto(
            int(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 0).text()), 
            str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 2).text()),
            str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 3).text()),
            str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 4).text())
        ),
        self.actualizarTablaRegistroMotos(),
         self.tablaRegistrosMotos.selectedItems() and generarTicketIngresoMoto(int(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 0).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 4).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 2).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 3).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 1).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 5).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 6).text()),
                                 )
        ])
        #Boton Limpiar Registro
        boton_LimpiarRegistro = QPushButton('LIMPIAR REGISTRO')
        boton_LimpiarRegistro .setStyleSheet(BOTONES['registros_boton_limpiar_registro'])
        layout_TablaRegistros.addWidget(boton_LimpiarRegistro, 8, 8, 1, 1)
        boton_LimpiarRegistro.clicked.connect(lambda: [ db_connection.limparRegistrosMotos(),
        self.actualizarTablaRegistroMotos()])
        #Hace que la fila 2 crezca 6 partes y la fila 8 crezca 1 parte
        layout_TablaRegistros.setRowStretch(2, 6)
        layout_TablaRegistros.setRowStretch(8, 1)

        #Se agrega el layout a la pagina
        page_TablaRegistros.setLayout(layout_TablaRegistros)
        #se agrega la pagina al stack
        self.stacked_widgetregistros.addWidget(page_TablaRegistros)

    def pantallaTablaFijos(self):
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        #Pagina de Usuarios
        page_TablaFijo = QWidget()
        #Layout de la Pagina de Usuarios
        layout_TablaFijo = QGridLayout()
        #------------------------------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_Fijo = QLabel('FIJO')
        titulo_Fijo.setStyleSheet(LABELS['registros_titulo_fijo'])
        layout_TablaFijo.addWidget(titulo_Fijo, 0, 0, 1, 9, Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINEAS['registros_linea_horizontal1_2'])
        layout_TablaFijo.addWidget(linea_horizontal1, 1, 0, 1, 9)
         # Crear la tabla de registros
        self.tablaRegistrosFijos = QTableWidget(self)
        self.tablaRegistrosFijos.setColumnCount(8)  # Definir el número de columnas
        self.tablaRegistrosFijos.verticalHeader().setVisible(False)
        self.tablaRegistrosFijos.setHorizontalHeaderLabels(
            ['ID', 'TIPO','NOTA','F.INGRESO', 'H.INGRESO', 'F.SALIDA', 'H.SALIDA','VALOR'])
        self.tablaRegistrosFijos.setStyleSheet(TABLAS['registros_tabla_registros_fijos'])
        #seleccionar toda la fila
        self.tablaRegistrosFijos.setSelectionBehavior(QAbstractItemView.SelectRows)
        #Configurar cabecera
        header = self.tablaRegistrosFijos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        #agregar la tabla
        layout_TablaFijo.addWidget(self.tablaRegistrosFijos, 2, 0, 6, 9)

        #Botones del filtro
        self.combobox_filtroRegistroFijos= QComboBox()
        self.combobox_filtroRegistroFijos.addItems(['Todo','ID','Tipo','Valor'])
        self.combobox_filtroRegistroFijos.setStyleSheet(COMBOBOX['registros_combobox_filtro_registro_fijos'])
        layout_TablaFijo.addWidget(self.combobox_filtroRegistroFijos, 8, 0, 1, 1)
        # Rellenar la tabla dependiendo de lo seleccionado en el combo box
        self.actualizarTablaFijos()

        self.textbox_FiltroRegistroFijo  = QLineEdit()
        self.textbox_FiltroRegistroFijo.setStyleSheet(INPUTS['registros_textbox_filtro_registro_fijo'])
        layout_TablaFijo.addWidget( self.textbox_FiltroRegistroFijo , 8, 1, 1, 1)

        #Boton Buscar 
        boton_Buscar = QPushButton('BUSCAR')
        boton_Buscar .setStyleSheet(BOTONES['registros_boton_buscar_2'])
        layout_TablaFijo.addWidget(boton_Buscar , 8, 2, 1, 1)
        boton_Buscar.clicked.connect(lambda: [
            self.actualizarTablaFijos()
            ])

        #Boton Reimprimir Registro
        boton_ReimprimirRegistro= QPushButton('REIMPRIMIR INGRESO')
        boton_ReimprimirRegistro .setStyleSheet(BOTONES['registros_boton_reimprimir_registro_2'])
        layout_TablaFijo.addWidget(boton_ReimprimirRegistro , 8, 5, 1, 1)
        boton_ReimprimirRegistro.clicked.connect(lambda: [
             self.tablaRegistrosFijos.selectedItems() and generarTicketIngresoFijo(int(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 0).text()),
                                 str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 3).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 4).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 1).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 2).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 7).text()),
        ),

        ])
        #Boton Eliminar Registro
        boton_EliminarRegistro= QPushButton('ELIMINAR REGISTRO')
        boton_EliminarRegistro .setStyleSheet(BOTONES['registros_boton_eliminar_registro_2'])
        layout_TablaFijo.addWidget(boton_EliminarRegistro , 8, 6, 1, 1)
        boton_EliminarRegistro.clicked.connect(lambda: [
            self.tablaRegistrosFijos.selectedItems() and db_connection.eliminarRegistroFijo(
                                int(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 0).text()),
                                 str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 5).text()),
        ),
        self.actualizarTablaFijos()])
        #Boton Guardar Edicion 
        boton_GuardarEdicion= QPushButton('GUARDAR EDICIÓN')
        boton_GuardarEdicion .setStyleSheet(BOTONES['registros_boton_guardar_edicion_2'])
        layout_TablaFijo.addWidget(boton_GuardarEdicion , 8, 7, 1, 1)
        boton_GuardarEdicion.clicked.connect(lambda: [
             self.tablaRegistrosFijos.selectedItems() and db_connection.editarRegistroFijo(
            int(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 0).text()), 
            str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 1).text()),
            str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 2).text()),
            str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 7).text())
        ),
        self.actualizarTablaFijos(),
         self.tablaRegistrosFijos.selectedItems() and generarTicketIngresoFijo(int(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 0).text()),
                                 str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 3).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 4).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 1).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 2).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 7).text()),
        )
        ])
        #Boton Limpiar Registro
        boton_Limpiar= QPushButton('LIMPIAR REGISTRO')
        boton_Limpiar .setStyleSheet(BOTONES['registros_boton_limpiar'])
        layout_TablaFijo.addWidget(boton_Limpiar, 8, 8, 1, 1)
        boton_Limpiar.clicked.connect(lambda: [ db_connection.limparRegistrosFijos(),
        self.actualizarTablaFijos()])
        #Fila-Tamaño
        layout_TablaFijo.setRowStretch(2, 6)
        layout_TablaFijo.setRowStretch(8, 1)
        #Se agrega el layout a la pagina
        page_TablaFijo.setLayout(layout_TablaFijo)
        #se agrega la pagina al stack
        self.stacked_widgetregistros.addWidget(page_TablaFijo)
    
    def pantallaTablaMensualidades(self):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)
        #Pagina de Usuarios
        page_TablaMensualidades = QWidget()
        #Layout de la Pagina de Usuarios
        layout_TablaMensualidades = QGridLayout()
        #------------------------------------------------------------
        # Crear el título y añadirlo a la sección izquierda
        titulo_Mensualidades = QLabel('MENSUALIDADES')
        titulo_Mensualidades.setStyleSheet(LABELS['registros_titulo_mensualidades'])
        layout_TablaMensualidades.addWidget(titulo_Mensualidades, 0, 0, 1, 9,Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINEAS['registros_linea_horizontal1_3'])
        layout_TablaMensualidades.addWidget(linea_horizontal1, 1, 0, 1, 9)
         # Crear la tabla de registros
        self.tabla_Mensualidades = QTableWidget(self)
        self.tabla_Mensualidades.setColumnCount(9)  # Definir el número de columnas
        self.tabla_Mensualidades.verticalHeader().setVisible(False)
        self.tabla_Mensualidades.setHorizontalHeaderLabels(
            ['ID', 'PLACA','NOMBRE', 'TELEFONO','F.INGRESO','H.INGRESO','F.U.PAGO','H.U.PAGO','F.RENOVACIÓN', 'D.TRANSCURRIDOS'])
        self.tabla_Mensualidades.setStyleSheet(TABLAS['registros_tabla_mensualidades'])
        #seleccionar toda la fila
        self.tabla_Mensualidades.setSelectionBehavior(QAbstractItemView.SelectRows)
        #Configurar cabecera      
        header = self.tabla_Mensualidades.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        layout_TablaMensualidades.addWidget(self.tabla_Mensualidades, 2, 0, 6, 9)

        #Botones del filtro
        self.combobox_FiltrarRegistrosMensualidad = QComboBox()
        self.combobox_FiltrarRegistrosMensualidad.addItems(['Todo', 'ID','Nombre','Telefono'])
        self.combobox_FiltrarRegistrosMensualidad.setStyleSheet(COMBOBOX['registros_combobox_filtrar_registros_mensualidad'])
        layout_TablaMensualidades.addWidget(self.combobox_FiltrarRegistrosMensualidad, 8, 0, 1, 1)
        
        self.textbox_FiltrarRegistrosMensualidad  = QLineEdit()
        self.textbox_FiltrarRegistrosMensualidad .setStyleSheet(INPUTS['registros_textbox_filtrar_registros_mensualidad'])
        layout_TablaMensualidades.addWidget(self.textbox_FiltrarRegistrosMensualidad , 8, 1, 1, 1)
        
        # Rellenar la tabla segun lo seleccionado en el combo box
        self.actualizarTablaMensualidades()
        #Boton Buscar 
        boton_Buscar = QPushButton('BUSCAR')
        boton_Buscar .setStyleSheet(BOTONES['registros_boton_buscar_3'])
        layout_TablaMensualidades.addWidget(boton_Buscar , 8, 2, 1, 1)
        boton_Buscar.clicked.connect(lambda: [
            self.actualizarTablaMensualidades()
            ])
        
        #Boton Reimprimir Registro
        boton_ReimprimirRegistro= QPushButton('REIMPRIMIR REGISTRO')
        boton_ReimprimirRegistro .setStyleSheet(BOTONES['registros_boton_reimprimir_registro_3'])
        layout_TablaMensualidades.addWidget(boton_ReimprimirRegistro , 8, 5, 1, 1)
        boton_ReimprimirRegistro.clicked.connect(lambda: [
            self.tabla_Mensualidades.selectedItems() and generarTicketIngresoMensualidad(int(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 0).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 4).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 5).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 2).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 1).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 3).text()),
        )])
        #Boton Guardar Edicion 
        boton_GuardarEdicion= QPushButton('GUARDAR EDICIÓN')
        boton_GuardarEdicion .setStyleSheet(BOTONES['registros_boton_guardar_edicion_3'])
        layout_TablaMensualidades.addWidget(boton_GuardarEdicion , 8, 6, 1, 1)
        boton_GuardarEdicion.clicked.connect(lambda: [
             self.tabla_Mensualidades.selectedItems() and db_connection.editarRegistroMensualidad(
            int(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 0).text()), 
            str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 1).text()),
            str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 2).text()),
            str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 3).text()),
            str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 8).text()),
        ),
        self.actualizarTablaMensualidades(),
         self.tabla_Mensualidades.selectedItems() and generarTicketRenovarMensualidad(
                                        int(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 0).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 6).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 7).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 2).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 1).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 3).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 8).text())
        )
        ])

        #Boton Limpiar Registro
        boton_Eliminar= QPushButton('ELIMINAR MENSUALIDAD')
        boton_Eliminar .setStyleSheet(BOTONES['registros_boton_eliminar'])
        layout_TablaMensualidades.addWidget(boton_Eliminar, 8, 7, 1, 1)
        boton_Eliminar.clicked.connect(lambda: [
            self.tabla_Mensualidades.selectedItems() and db_connection.eliminarRegistroMensualidades(
                                int(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 0).text()),
                                 str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 8).text()),
        ),
        self.actualizarTablaMensualidades()])
        #Fila-Tamaño
        #Fila-Tamaño
        layout_TablaMensualidades.setRowStretch(2, 6)
        layout_TablaMensualidades.setRowStretch(8, 1)
        #Se agrega el layout a la pagina
        page_TablaMensualidades.setLayout(layout_TablaMensualidades)
        #se agrega la pagina al stack
        self.stacked_widgetregistros.addWidget(page_TablaMensualidades)

    def pantallaTablaResumen(self):
        # Crear la instancia de DatabaseConnection
        db_connection = DatabaseConnection.get_instance(DB_CONFIG)

        # Página de Resumen
        page_TablaResumen = QWidget()
        # Layout de la Página de Resumen
        layout_TablaResumen = QGridLayout()
        
        #------------------------------------------------------------
        # Crear el título y añadirlo a la sección superior
        titulo_Resumen = QLabel('RESUMEN')
        titulo_Resumen.setStyleSheet(LABELS['registros_titulo_resumen'])
        layout_TablaResumen.addWidget(titulo_Resumen, 0, 0, 1, 9, alignment=Qt.AlignCenter)
        
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet(LINEAS['registros_linea_horizontal1_4'])
        layout_TablaResumen.addWidget(linea_horizontal1, 1, 0, 1, 9)
        
        # Crear labels para mostrar la información del resumen
        # Fecha y Hora
        self.label_fecha = QLabel('Fecha: Cargando...')
        self.label_fecha.setStyleSheet(LABELS['registros_label_fecha'])
        layout_TablaResumen.addWidget(self.label_fecha, 2, 0, 1, 3)
        
        self.label_hora = QLabel('Hora: Cargando...')
        self.label_hora.setStyleSheet(LABELS['registros_label_hora'])
        layout_TablaResumen.addWidget(self.label_hora, 2, 3, 1, 3)
        
        # Información de registros por Día
        self.label_registros_dia = QLabel('Registros Día: 0')
        self.label_registros_dia.setStyleSheet(LABELS['registros_label_registros_dia'])
        layout_TablaResumen.addWidget(self.label_registros_dia, 3, 0, 1, 3)
        
        self.label_total_dia = QLabel('Total Día: $0')
        self.label_total_dia.setStyleSheet(LABELS['registros_label_total_dia'])
        layout_TablaResumen.addWidget(self.label_total_dia, 3, 3, 1, 3)
        
        # Información de registros por Hora
        self.label_registros_hora = QLabel('Registros Hora: 0')
        self.label_registros_hora.setStyleSheet(LABELS['registros_label_registros_hora'])
        layout_TablaResumen.addWidget(self.label_registros_hora, 4, 0, 1, 3)
        
        self.label_total_hora = QLabel('Total Hora: $0')
        self.label_total_hora.setStyleSheet(LABELS['registros_label_total_hora'])
        layout_TablaResumen.addWidget(self.label_total_hora, 4, 3, 1, 3)
        
        # Información de Mensualidades
        self.label_registros_mes = QLabel('Registros Mensualidades: 0')
        self.label_registros_mes.setStyleSheet(LABELS['registros_label_registros_mes'])
        layout_TablaResumen.addWidget(self.label_registros_mes, 5, 0, 1, 3)
        
        self.label_total_mes = QLabel('Total Mensualidades: $0')
        self.label_total_mes.setStyleSheet(LABELS['registros_label_total_mes'])
        layout_TablaResumen.addWidget(self.label_total_mes, 5, 3, 1, 3)
        
        # Información de Fijos
        self.label_registros_fijos = QLabel('Registros Fijos: 0')
        self.label_registros_fijos.setStyleSheet(LABELS['registros_label_registros_fijos'])
        layout_TablaResumen.addWidget(self.label_registros_fijos, 6, 0, 1, 3)
        
        self.label_total_fijos = QLabel('Total Fijos: $0')
        self.label_total_fijos.setStyleSheet(LABELS['registros_label_total_fijos'])
        layout_TablaResumen.addWidget(self.label_total_fijos, 6, 3, 1, 3)
        
        # Línea separadora
        linea_horizontal2 = QFrame()
        linea_horizontal2.setFrameShape(QFrame.HLine)
        linea_horizontal2.setLineWidth(2)
        linea_horizontal2.setStyleSheet(LINEAS['registros_linea_horizontal2_2'])
        layout_TablaResumen.addWidget(linea_horizontal2, 7, 0, 1, 9)
        
        # Total Registros (suma de todos los registros)
        self.label_total_registros = QLabel('TOTAL REGISTROS: 0')
        self.label_total_registros.setStyleSheet(LABELS['registros_label_total_registros'])
        layout_TablaResumen.addWidget(self.label_total_registros, 8, 0, 1, 4, alignment=Qt.AlignCenter)
        
        # Total General (suma de todos los valores monetarios)
        self.label_total_general = QLabel('TOTAL GENERAL: $0')
        self.label_total_general.setStyleSheet(LABELS['registros_label_total_general'])
        layout_TablaResumen.addWidget(self.label_total_general, 8, 5, 1, 4, alignment=Qt.AlignCenter)
        
        # Botón para actualizar el resumen
        boton_ActualizarResumen = QPushButton('ACTUALIZAR RESUMEN')
        boton_ActualizarResumen.setStyleSheet(BOTONES['registros_boton_actualizar_resumen'])
        layout_TablaResumen.addWidget(boton_ActualizarResumen, 9, 3, 1, 3, alignment=Qt.AlignCenter)
        boton_ActualizarResumen.clicked.connect(lambda: self.actualizarResumen())
        
        # Configurar el stretch para que el contenido se distribuya bien
        layout_TablaResumen.setRowStretch(2, 1)
        layout_TablaResumen.setRowStretch(3, 1)
        layout_TablaResumen.setRowStretch(4, 1)
        layout_TablaResumen.setRowStretch(5, 1)
        layout_TablaResumen.setRowStretch(6, 1)
        layout_TablaResumen.setRowStretch(8, 1)
        layout_TablaResumen.setRowStretch(9, 1)
        
        # Se agrega el layout a la página
        page_TablaResumen.setLayout(layout_TablaResumen)
        # Se agrega la página al stack
        self.stacked_widgetregistros.addWidget(page_TablaResumen)
        
        # Cargar los datos automáticamente al crear la pantalla
        self.actualizarResumen()

    def actualizarResumen(self):
        """Función para actualizar los datos del resumen consultando la base de datos"""
        try:
            # Verificar que los labels existen antes de actualizar
            if not hasattr(self, 'label_fecha'):
                print("Los labels del resumen no están inicializados")
                return
                
            # Crear la instancia de DatabaseConnection
            db_connection = DatabaseConnection.get_instance(DB_CONFIG)
            
            # Consultar los datos de resumen de hoy
            datos_resumen = db_connection.consultarResumenHoy()
            
            # Obtener fecha y hora actual
            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            hora_actual = datetime.now().strftime('%H:%M:%S')
            
            # Actualizar los labels con los datos obtenidos
            self.label_fecha.setText(f'Fecha: {fecha_actual}')
            self.label_hora.setText(f'Hora: {hora_actual}')
            
            # Actualizar información de registros por Día
            self.label_registros_dia.setText(f'Registros Día: {datos_resumen["registrosDia"]}')
            self.label_total_dia.setText(f'Total Día: ${datos_resumen["totalDia"]:,.0f}')
            
            # Actualizar información de registros por Hora
            self.label_registros_hora.setText(f'Registros Hora: {datos_resumen["registrosHora"]}')
            self.label_total_hora.setText(f'Total Hora: ${datos_resumen["totalHora"]:,.0f}')
            
            # Actualizar información de Mensualidades
            self.label_registros_mes.setText(f'Registros Mensualidades: {datos_resumen["registrosMes"]}')
            self.label_total_mes.setText(f'Total Mensualidades: ${datos_resumen["totalMes"]:,.0f}')
            
            # Actualizar información de Fijos
            self.label_registros_fijos.setText(f'Registros Fijos: {datos_resumen["registrosFijos"]}')
            self.label_total_fijos.setText(f'Total Fijos: ${datos_resumen["totalFijos"]:,.0f}')
            
            # Calcular Total de Registros (suma de todos los tipos de registros)
            total_registros = (datos_resumen["registrosHora"] + 
                            datos_resumen["registrosDia"] + 
                            datos_resumen["registrosMes"] + 
                            datos_resumen["registrosFijos"])
            
            # Actualizar Total de Registros
            self.label_total_registros.setText(f'TOTAL REGISTROS: {total_registros:,}')
            
            # Actualizar Total General
            self.label_total_general.setText(f'TOTAL GENERAL: ${datos_resumen["totalGeneral"]:,.0f}')
            
        except Exception as e:
            # En caso de error, mostrar mensaje en consola
            print(f"Error al actualizar resumen: {e}")
            # Solo intentar actualizar labels si existen
            if hasattr(self, 'label_fecha'):
                self.label_fecha.setText('Error al cargar datos')
            if hasattr(self, 'label_hora'):
                self.label_hora.setText('Error al cargar datos')
            # También verificar si existe el nuevo label antes de actualizarlo
            if hasattr(self, 'label_total_registros'):
                self.label_total_registros.setText('Error al cargar datos')