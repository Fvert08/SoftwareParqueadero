MESSAGE_BOX_STYLE = """
QMessageBox {
    background-color: #151419;
    color: white;
}
QLabel { color: white; }
QPushButton {
    color: white;
    border: 1px solid white;
    background-color: transparent;
    padding: 5px 15px;
    border-radius: 5px;
}
QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.15);
}
"""

TEXTBOX_STYLE_30 = "color: #FFFFFF; margin: 0; padding: 0; font-size: 30px;"
TITLE_STYLE_30_WHITE_BOLD = "color: #FFFFFF;font-size: 30px; font-weight: bold;"
LINE_STYLE_WHITE = "color: #FFFFFF;"
LABEL_STYLE_30_WHITE = "color: #FFFFFF;font-size: 30px;"
TITLE_STYLE_30_GRAY_BOLD = "color: #888888;font-size: 30px; font-weight: bold;"
LABEL_STYLE_40_WHITE = "color: #FFFFFF;font-size: 40px;"
BUTTON_STYLE_DARK_RADIUS_10 = "color: White; background-color: #222125; border-radius: 15px; padding: 10px;"
TITLE_STYLE_40_WHITE_BOLD = "color: #FFFFFF;font-size: 40px; font-weight: bold;"
TITLE_STYLE_20_WHITE_BOLD = "color: #FFFFFF;font-size: 20px; font-weight: bold;"

TABLE_STYLE_DARK = """
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
        """

BUTTON_STYLE_DARK_15_10_20 = "color: White; background-color: #222125; font-size: 15px; border-radius: 15px; padding: 10px 20px;"
BUTTON_STYLE_DARK_25_10_20 = "color: White; background-color: #222125; font-size: 25px; border-radius: 15px; padding: 10px 20px;"
BUTTON_STYLE_TICKETS_DISABLED = """
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #666666;
            }
            QPushButton:disabled:hover {
                background-color: #3a3a3a;
                color: #666666;
                border: none;
            }
            QPushButton:disabled:pressed {
                background-color: #3a3a3a;
                color: #666666;
                border: none;
            }
        """
LABEL_STYLE_18_WHITE = "color: #FFFFFF; font-size: 18px;"
LABEL_STYLE_18_GREEN_BOLD = "color: #00FF00; font-size: 18px; font-weight: bold;"
TEXTBOX_STYLE_40 = "color: #FFFFFF; margin: 0; padding: 0;font-size: 40px;"
TEXTBOX_STYLE_20 = "color: #FFFFFF; margin: 0; padding: 0;font-size: 20px;"
BUTTON_STYLE_DARK_35_10_20 = "color: White; background-color: #222125; font-size: 35px; border-radius: 15px; padding: 10px 20px;"
BUTTON_STYLE_DARK_30_10_20 = "color: White; background-color: #222125; font-size: 30px; border-radius: 15px; padding: 10px 20px;"
BUTTON_STYLE_TICKETS_PRIMARY = """
            QPushButton {
                color: white; 
                background-color: #222125; 
                font-size: 30px; 
                border-radius: 15px; 
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #444444;
                color: lightgray;
                border: 2px solid #555555;
            }
        """
BUTTON_STYLE_MAIN_ACTIVE = "background-color: #222125; color: White; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;"
BUTTON_STYLE_DARK_RADIUS_COMPACT = "color: White; background-color: #222125;border-radius: 15px; padding: 10px;"
LABEL_STYLE_30_WHITE_SPACED = "color: #FFFFFF; font-size: 30px;"
LABEL_STYLE_20_WHITE_BOLD_SPACED = "color: #FFFFFF; font-size: 20px; font-weight: bold;"
CALENDAR_FONT_SIZE_30 = "font-size: 30px;"
CALENDAR_STYLE_DARK = "background-color: #222126; color: white; font-size: 30px; alternate-background-color: #131216;"

BUTTON_STYLE_MAIN_INACTIVE = "QPushButton{background-color:#151419;color:#737074;border:none;border-radius:15px;font-size:12px;text-align:left;padding-left:10px;font-weight:bold;min-height:60px;min-width:200px;}QPushButton:hover{background-color:#1f1e24;color:#ffffff;}"
