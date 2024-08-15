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

            item_fecha_salida = QTableWidgetItem(registro.get('fechaSalida', '').strftime('%Y-%m-%d') if isinstance(registro.get('fechaSalida', ''), (datetime, date)) else str(registro.get('fechaSalida', '')))
            item_fecha_salida.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 7, item_fecha_salida)

            item_hora_salida = QTableWidgetItem(str(registro.get('horaSalida', '')))
            item_hora_salida.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 8, item_hora_salida)

            item_total = QTableWidgetItem(str(registro.get('Total', '')))
            item_total.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosMotos.setItem(row_idx, 9, item_total)

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

            item_fecha_salida = QTableWidgetItem(registro.get('fechaSalida', '').strftime('%Y-%m-%d') if isinstance(registro.get('fechaSalida', ''), (datetime, date)) else str(registro.get('fechaSalida', '')))
            item_fecha_salida.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 5, item_fecha_salida)

            item_hora_salida = QTableWidgetItem(str(registro.get('horaSalida', '')))
            item_hora_salida.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 6, item_hora_salida)

            item_total = QTableWidgetItem(str(registro.get('Valor', '')))
            item_total.setTextAlignment(Qt.AlignCenter)
            self.tablaRegistrosFijos.setItem(row_idx, 7, item_total)

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
        #------------------------Menu lateral---------------------------
        # Crear la línea vertical de 1 pixel y añadirla a la cuadrícula
        linea_vertical = QFrame()
        linea_vertical.setFrameShape(QFrame.VLine)
        linea_vertical.setLineWidth(1)
        linea_vertical.setStyleSheet("color: #FFFFFF;")
        layout_registros.addWidget(linea_vertical, 0, 0, 8, 1)
        # Crear la sección derecha con el título "Menú"
        titulo_menu = QLabel('MENÚ')
        titulo_menu.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_registros.addWidget(titulo_menu, 0, 1, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)

        linea_horizontal2 = QFrame()
        linea_horizontal2.setFrameShape(QFrame.HLine)
        linea_horizontal2.setLineWidth(1)
        linea_horizontal2.setStyleSheet("color: #FFFFFF;")
        layout_registros.addWidget(linea_horizontal2, 0, 1, 1, 2, alignment=Qt.AlignBottom)
        # Crea un boton para cambiar a Registros
        boton_Registros= QPushButton("REGISTROS")
        boton_Registros.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_registros.addWidget(boton_Registros, 1, 1, 1, 1, alignment=Qt.AlignHCenter  | Qt.AlignCenter)
        boton_Registros.setCheckable(True)
        boton_Registros.setChecked(True)
        boton_Registros.pressed.connect(lambda: self.stacked_widgetregistros.setCurrentIndex(0))
        # Crea un boton para cambiar a Fijos
        boton_Fijos = QPushButton("FIJOS")
        boton_Fijos.setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_registros.addWidget(boton_Fijos, 2, 1, 1, 1, alignment=Qt.AlignHCenter | Qt.AlignCenter)
        boton_Fijos.setCheckable(True)
        boton_Fijos.pressed.connect(lambda: self.stacked_widgetregistros.setCurrentIndex(1))
      
        # Crea un boton para cambiar a las Mensualidades
        boton_Mensualidades = QPushButton("MENSUALIDADES")
        boton_Mensualidades.setStyleSheet("color: White; background-color: #222125; font-size: 10px; border-radius: 15px; padding: 10px 20px;")
        layout_registros.addWidget(boton_Mensualidades, 3, 1, 1, 1, alignment=Qt.AlignHCenter  |Qt.AlignCenter)
        boton_Mensualidades.setCheckable(True)
        boton_Mensualidades.pressed.connect(lambda: self.stacked_widgetregistros.setCurrentIndex(2))

        layout_registros.setRowStretch(0, 0)
        layout_registros.setRowStretch(1, 1)
        layout_registros.setRowStretch(2, 1)
        layout_registros.setRowStretch(3, 1)
        layout_registros.setRowStretch(4, 1)
        layout_registros.setRowStretch(5, 1)
        layout_registros.setRowStretch(6, 1)
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
        titulo_Registros.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_TablaRegistros.addWidget(titulo_Registros, 0, 0, 1, 9, alignment=Qt.AlignTop | Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_TablaRegistros.addWidget(linea_horizontal1, 0, 0, 1, 9, alignment=Qt.AlignBottom)
         # Crear la tabla de registros
        self.tablaRegistrosMotos = QTableWidget(self)
        self.tablaRegistrosMotos.setColumnCount(10)  # Definir el número de columnas
        self.tablaRegistrosMotos.verticalHeader().setVisible(False)
        self.tablaRegistrosMotos.setHorizontalHeaderLabels(
            ['ID', 'CASILLERO', 'PLACA', 'CASCOS', 'TIPO', 'F.INGRESO', 'H.INGRESO', 'F.SALIDA','H.SALIDA', 'TOTAL'])
        self.tablaRegistrosMotos.setStyleSheet("""
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
        self.tablaRegistrosMotos.setSelectionBehavior(QAbstractItemView.SelectRows)
        #Configurar cabecera
        header = self.tablaRegistrosMotos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        #Botones del filtro
        layout_TablaRegistros.addWidget(self.tablaRegistrosMotos, 1, 0, 7, 9)
        self.combobox_FiltroRegistroMoto = QComboBox()
        self.combobox_FiltroRegistroMoto.addItems(['Todo', "ID" ,'Casillero', 'Placa', 'Tipo'])
        self.combobox_FiltroRegistroMoto.setFixedWidth(130)
        self.combobox_FiltroRegistroMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 30px;")
        layout_TablaRegistros.addWidget(self.combobox_FiltroRegistroMoto, 8, 0, 1, 1, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        
        self.textbox_FiltroRegistroMoto = QLineEdit()
        self.textbox_FiltroRegistroMoto.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        self.textbox_FiltroRegistroMoto.setFixedWidth(250)
        layout_TablaRegistros.addWidget(self.textbox_FiltroRegistroMoto , 8, 1, 1, 1, alignment=Qt.AlignBottom |Qt.AlignHCenter)
        # Rellenar la tabla
        self.actualizarTablaRegistroMotos()
        #Boton Buscar 
        boton_Buscar = QPushButton('BUSCAR')
        boton_Buscar .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaRegistros.addWidget(boton_Buscar , 8, 2, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_Buscar.clicked.connect(lambda: [
            self.actualizarTablaRegistroMotos()
            ])
        #Boton Reimprimir Registro
        boton_ReimprimirRegistro= QPushButton('REIMPRIMIR INGRESO')
        boton_ReimprimirRegistro .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaRegistros.addWidget(boton_ReimprimirRegistro , 8, 5, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_ReimprimirRegistro.clicked.connect(lambda: [
            generarTicketIngresoMoto(int(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 0).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 4).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 2).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 3).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 1).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 5).text()),
                                 str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 6).text()),
        )])
        #Boton Eliminar Registro
        boton_EliminarRegistro= QPushButton('ELIMINAR REGISTRO')
        boton_EliminarRegistro .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaRegistros.addWidget(boton_EliminarRegistro , 8, 6, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        #Boton Guardar Edicion 
        boton_GuardarEdicion= QPushButton('GUARDAR EDICIÓN')
        boton_GuardarEdicion .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaRegistros.addWidget(boton_GuardarEdicion , 8, 7, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_GuardarEdicion.clicked.connect(lambda: [
            db_connection.editarRegistroMoto(
            int(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 0).text()), 
            str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 2).text()),
            str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 3).text()),
            str(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 4).text())
        ),
        self.actualizarTablaRegistroMotos("Todo","0"),
        generarTicketIngresoMoto(int(self.tablaRegistrosMotos.item(self.tablaRegistrosMotos.currentRow(), 0).text()),
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
        boton_LimpiarRegistro .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaRegistros.addWidget(boton_LimpiarRegistro, 8, 8, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        #Fila-Tamaño
        layout_TablaRegistros.setRowStretch(0, 0)
        layout_TablaRegistros.setRowStretch(1, 1)
        layout_TablaRegistros.setRowStretch(2, 1)
        layout_TablaRegistros.setRowStretch(3, 1)
        layout_TablaRegistros.setRowStretch(4, 1)
        layout_TablaRegistros.setRowStretch(5, 1)
        layout_TablaRegistros.setRowStretch(6, 1)
        layout_TablaRegistros.setRowStretch(7, 2)
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
        titulo_Fijo.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_TablaFijo.addWidget(titulo_Fijo, 0, 0, 1, 9, alignment=Qt.AlignTop | Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_TablaFijo.addWidget(linea_horizontal1, 0, 0, 1, 9, alignment=Qt.AlignBottom)
         # Crear la tabla de registros
        self.tablaRegistrosFijos = QTableWidget(self)
        self.tablaRegistrosFijos.setColumnCount(8)  # Definir el número de columnas
        self.tablaRegistrosFijos.verticalHeader().setVisible(False)
        self.tablaRegistrosFijos.setHorizontalHeaderLabels(
            ['ID', 'TIPO','NOTA','F.INGRESO', 'H.INGRESO', 'F.SALIDA', 'H.SALIDA','VALOR'])
        self.tablaRegistrosFijos.setStyleSheet("""
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
        self.tablaRegistrosFijos.setSelectionBehavior(QAbstractItemView.SelectRows)
         #Configurar cabecera
        header = self.tablaRegistrosFijos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        #agregar la tabla
        layout_TablaFijo.addWidget(self.tablaRegistrosFijos, 1, 0, 7, 9)

        self.combobox_filtroRegistroFijos= QComboBox()
        self.combobox_filtroRegistroFijos.addItems(['Todo','ID','Tipo','Valor'])
        self.combobox_filtroRegistroFijos.setFixedWidth(130)
        self.combobox_filtroRegistroFijos.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 30px;")
        layout_TablaFijo.addWidget(self.combobox_filtroRegistroFijos, 8, 0, 1, 1, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        
        self.textbox_FiltroRegistroFijo  = QLineEdit()
        self.textbox_FiltroRegistroFijo.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        self.textbox_FiltroRegistroFijo .setFixedWidth(250)
        layout_TablaFijo.addWidget( self.textbox_FiltroRegistroFijo , 8, 1, 1, 1, alignment=Qt.AlignBottom |Qt.AlignHCenter)


        # Rellenar la tabla
        self.actualizarTablaFijos()
        #Boton Buscar 
        boton_Buscar = QPushButton('BUSCAR')
        boton_Buscar .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaFijo.addWidget(boton_Buscar , 8, 2, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_Buscar.clicked.connect(lambda: [
            self.actualizarTablaFijos()
            ])

        #Boton Reimprimir Registro
        boton_ReimprimirRegistro= QPushButton('REIMPRIMIR INGRESO')
        boton_ReimprimirRegistro .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaFijo.addWidget(boton_ReimprimirRegistro , 8, 5, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_ReimprimirRegistro.clicked.connect(lambda: [
            generarTicketIngresoFijo(int(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 0).text()),
                                 str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 3).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 4).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 1).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 2).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 7).text()),
        ),

        ])
        #Boton Eliminar Registro
        boton_EliminarRegistro= QPushButton('ELIMINAR REGISTRO')
        boton_EliminarRegistro .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaFijo.addWidget(boton_EliminarRegistro , 8, 6, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        #Boton Guardar Edicion 
        boton_GuardarEdicion= QPushButton('GUARDAR EDICIÓN')
        boton_GuardarEdicion .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaFijo.addWidget(boton_GuardarEdicion , 8, 7, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_GuardarEdicion.clicked.connect(lambda: [
            db_connection.editarRegistroFijo(
            int(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 0).text()), 
            str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 1).text()),
            str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 2).text()),
            str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 7).text())
        ),
        self.actualizarTablaFijos(),
        generarTicketIngresoFijo(int(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 0).text()),
                                 str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 3).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 4).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 1).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 2).text()),
                                str(self.tablaRegistrosFijos.item(self.tablaRegistrosFijos.currentRow(), 7).text()),
        )
        ])
        #Boton Limpiar Registro
        boton_Limpiar= QPushButton('LIMPIAR REGISTRO')
        boton_Limpiar .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaFijo.addWidget(boton_Limpiar, 8, 8, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        #Fila-Tamaño
        layout_TablaFijo.setRowStretch(0, 0)
        layout_TablaFijo.setRowStretch(1, 1)
        layout_TablaFijo.setRowStretch(2, 1)
        layout_TablaFijo.setRowStretch(3, 1)
        layout_TablaFijo.setRowStretch(4, 1)
        layout_TablaFijo.setRowStretch(5, 1)
        layout_TablaFijo.setRowStretch(6, 1)
        layout_TablaFijo.setRowStretch(7, 2)
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
        titulo_Mensualidades.setStyleSheet("color: #888888;font-size: 30px; font-weight: bold;")
        layout_TablaMensualidades.addWidget(titulo_Mensualidades, 0, 0, 1, 9, alignment=Qt.AlignTop | Qt.AlignCenter)
        # Crear la línea horizontal de 1 pixel y añadirla a la cuadrícula
        linea_horizontal1 = QFrame()
        linea_horizontal1.setFrameShape(QFrame.HLine)
        linea_horizontal1.setLineWidth(1)
        linea_horizontal1.setStyleSheet("color: #FFFFFF;")
        layout_TablaMensualidades.addWidget(linea_horizontal1, 0, 0, 1, 9, alignment=Qt.AlignBottom)
         # Crear la tabla de registros
        self.tabla_Mensualidades = QTableWidget(self)
        self.tabla_Mensualidades.setColumnCount(9)  # Definir el número de columnas
        self.tabla_Mensualidades.verticalHeader().setVisible(False)
        self.tabla_Mensualidades.setHorizontalHeaderLabels(
            ['ID', 'PLACA','NOMBRE', 'TELEFONO','F.INGRESO','H.INGRESO','F.U.PAGO','H.U.PAGO','F.RENOVACIÓN', 'D.TRANSCURRIDOS'])
        self.tabla_Mensualidades.setStyleSheet("""
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
        self.tabla_Mensualidades.setSelectionBehavior(QAbstractItemView.SelectRows)
        #Configurar cabecera      
        header = self.tabla_Mensualidades.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Estirar las columnas para ocupar el espacio
        header.setStretchLastSection(True)  # Estirar la última sección (última columna) para llenar el espacio restante
        layout_TablaMensualidades.addWidget(self.tabla_Mensualidades, 1, 0, 7, 9)

        

        self.combobox_FiltrarRegistrosMensualidad = QComboBox()
        self.combobox_FiltrarRegistrosMensualidad.addItems(['Todo', 'ID','Nombre','Telefono'])
        self.combobox_FiltrarRegistrosMensualidad.setFixedWidth(130)
        self.combobox_FiltrarRegistrosMensualidad.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0;font-size: 30px;")
        layout_TablaMensualidades.addWidget(self.combobox_FiltrarRegistrosMensualidad, 8, 0, 1, 1, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        
        self.textbox_FiltrarRegistrosMensualidad  = QLineEdit()
        self.textbox_FiltrarRegistrosMensualidad .setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;")
        self.textbox_FiltrarRegistrosMensualidad .setFixedWidth(200)
        layout_TablaMensualidades.addWidget(self.textbox_FiltrarRegistrosMensualidad , 8, 1, 1, 1, alignment=Qt.AlignBottom |Qt.AlignHCenter)
        
        # Rellenar la tabla
        self.actualizarTablaMensualidades()
        #Boton Buscar 
        boton_Buscar = QPushButton('BUSCAR')
        boton_Buscar .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaMensualidades.addWidget(boton_Buscar , 8, 2, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_Buscar.clicked.connect(lambda: [
            self.actualizarTablaMensualidades()
            ])
        
        #Boton Reimprimir Registro
        boton_ReimprimirRegistro= QPushButton('REIMPRIMIR REGISTRO')
        boton_ReimprimirRegistro .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaMensualidades.addWidget(boton_ReimprimirRegistro , 8, 6, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_ReimprimirRegistro.clicked.connect(lambda: [
            generarTicketIngresoMensualidad(int(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 0).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 4).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 5).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 2).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 1).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 3).text()),
        )])
        #Boton Guardar Edicion 
        boton_GuardarEdicion= QPushButton('GUARDAR EDICIÓN')
        boton_GuardarEdicion .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaMensualidades.addWidget(boton_GuardarEdicion , 8, 7, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_GuardarEdicion.clicked.connect(lambda: [
            db_connection.editarRegistroMensualidad(
            int(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 0).text()), 
            str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 1).text()),
            str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 2).text()),
            str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 3).text())
        ),
        self.actualizarTablaMensualidades(),
        generarTicketIngresoMensualidad(int(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 0).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 4).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 5).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 2).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 1).text()),
                                        str(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 3).text()),
        )
        ])

        #Boton Limpiar Registro
        boton_Eliminar= QPushButton('ELIMINAR MENSUALIDAD')
        boton_Eliminar .setStyleSheet("color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;")
        layout_TablaMensualidades.addWidget(boton_Eliminar, 8, 8, 1, 1,
                                alignment=Qt.AlignBottom| Qt.AlignHCenter)
        boton_Eliminar.clicked.connect(lambda: [
            db_connection.eliminarMensualidad(
            int(self.tabla_Mensualidades.item(self.tabla_Mensualidades.currentRow(), 0).text()), 
        ),
        self.actualizarTablaMensualidades()
        ])
        #Fila-Tamaño
        layout_TablaMensualidades.setRowStretch(0, 0)
        layout_TablaMensualidades.setRowStretch(1, 1)
        layout_TablaMensualidades.setRowStretch(2, 1)
        layout_TablaMensualidades.setRowStretch(3, 1)
        layout_TablaMensualidades.setRowStretch(4, 1)
        layout_TablaMensualidades.setRowStretch(5, 1)
        layout_TablaMensualidades.setRowStretch(6, 1)
        layout_TablaMensualidades.setRowStretch(7, 2)
        layout_TablaMensualidades.setRowStretch(8, 1)
        #Se agrega el layout a la pagina
        page_TablaMensualidades.setLayout(layout_TablaMensualidades)
        #se agrega la pagina al stack
        self.stacked_widgetregistros.addWidget(page_TablaMensualidades)

