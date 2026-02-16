# =========================
# MENSAJES
# =========================
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

LABEL_MENSAJE = "QLabel { color: white; }"
BOTON_MENSAJE = """
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


# =========================
# BOTONES LATERALES
# =========================
BOTON_LATERAL_ACTIVO = "background-color: #222125; color: White; border: none; border-radius: 15px;font-size: 12px;text-align: left;padding-left: 10px;font-weight: bold;min-height: 60px;min-width: 200px;"
BOTON_LATERAL_INACTIVO = "QPushButton{background-color:#151419;color:#737074;border:none;border-radius:15px;font-size:12px;text-align:left;padding-left:10px;font-weight:bold;min-height:60px;min-width:200px;}QPushButton:hover{background-color:#1f1e24;color:#ffffff;}"


def boton_lateral(tamano=15, padding="10px 20px", negrita=True):
    peso = "font-weight:bold;" if negrita else ""
    return (
        "QPushButton{color:#737074;background-color:#151419;font-size:"
        + str(tamano)
        + "px;border:none;border-radius:15px;padding:"
        + padding
        + ";"
        + peso
        + "}"
        "QPushButton:hover{background-color:#1f1e24;color:#ffffff;}"
        "QPushButton:checked{background-color:#222125;color:#ffffff;}"
        "QPushButton:checked:hover{background-color:#222125;color:#ffffff;}"
    )


# =========================
# BOTONES FORMULARIO
# =========================
def boton_formulario(tamano=15, padding="10px 20px"):
    return f"color: White; background-color: #222125; font-size: {tamano}px; border-radius: 15px; padding: {padding};"


BOTON_FORMULARIO_MINI = "color: White; background-color: #222125; border-radius: 15px; padding: 10px;"
BOTON_FORMULARIO_TABLA = "color: White; background-color: #222125; border-radius: 15px; padding: 10px;"
BOTON_FORMULARIO_RESUMEN = "color: White; background-color: #222125; border-radius: 15px; padding: 15px; font-size: 16px;"
BOTON_FORMULARIO_DARK = "color: White; background-color: #151419; font-size: 30px; border-radius: 1px; padding: 10px 10px;"


def boton_formulario_presion(tamano=30, padding="15px 30px", deshabilitado=False):
    estilo = (
        "QPushButton {"
        "color: white; "
        "background-color: #222125; "
        f"font-size: {tamano}px; "
        "border-radius: 15px; "
        f"padding: {padding};"
        "}"
        "QPushButton:pressed {"
        "background-color: #444444;"
        "color: lightgray;"
        "border: 2px solid #555555;"
        "}"
    )
    if deshabilitado:
        estilo += (
            "QPushButton:disabled {"
            "background-color: #3a3a3a;"
            "color: #666666;"
            "}"
            "QPushButton:disabled:hover {"
            "background-color: #3a3a3a;"
            "color: #666666;"
            "border: none;"
            "}"
            "QPushButton:disabled:pressed {"
            "background-color: #3a3a3a;"
            "color: #666666;"
            "border: none;"
            "}"
        )
    return estilo


# =========================
# CAMPOS DE TEXTO
# =========================
def campo_texto(tamano=30, color="#FFFFFF"):
    return f"color: {color}; margin: 0; padding: 0; font-size: {tamano}px;"


CAMPO_TEXTO_30 = campo_texto(30)
CAMPO_TEXTO_40 = "color: #FFFFFF; margin: 0; padding: 0;font-size: 40px;"
CAMPO_TEXTO_20 = "color: #FFFFFF; margin: 0; padding: 0;font-size: 20px;"
CAMPO_TEXTO_VERDE_30 = "color: #89d631 ; margin: 0; padding: 0; font-size: 30px;"


# =========================
# TABLAS
# =========================
TABLA_ESTANDAR = """
QTableWidget {
    background-color: #222126;
    color: white;
    border: 1px solid #222126;
    alternate-background-color: #131216;
}
QTableWidget::item {
    background-color: #151419;
    border: 0px solid #222126;
}
QTableWidget::item:hover {
    background-color: #2a292e;
}
QTableWidget::item:selected {
    background-color: #3c3b40;
    color: white;
}
QHeaderView::section {
    background-color: #151419;
    color: white;
    border: none;
    padding: 4px;
}
QHeaderView::section:hover {
    background-color: #2a292e;
}
QHeaderView::section:selected {
    background-color: white;
    color: white;
}
QLineEdit {
    color: white;
}
"""


# =========================
# TEXTOS Y LÍNEAS
# =========================
LINEA_BLANCA = "color: #FFFFFF;"
LINEA_OSCURA = "color: #222126;"
FONDO_OSCURO = "background-color: #151419;"

TITULO_SECCION = "color: #888888;font-size: 30px; font-weight: bold;"
TITULO_SECCION_25 = "color: #888888;font-size: 25px; font-weight: bold;"
TITULO_PAGINA = "color: #888888; font-size: 20px; font-weight: bold;"
TITULO_BLANCO_40 = "color: #FFFFFF;font-size: 40px; font-weight: bold;"
TITULO_BLANCO_30 = "color: #FFFFFF;font-size: 30px; font-weight: bold;"
TITULO_BLANCO_20 = "color: #FFFFFF;font-size: 20px; font-weight: bold;"

TEXTO_BLANCO_40 = "color: #FFFFFF;font-size: 40px;"
TEXTO_BLANCO_30 = "color: #FFFFFF;font-size: 30px;"
TEXTO_BLANCO_30_ESP = "color: #FFFFFF; font-size: 30px;"
TEXTO_BLANCO_20 = "color: #FFFFFF; font-size: 20px;"
TEXTO_BLANCO_20_BOLD = "color: #FFFFFF; font-size: 20px; font-weight: bold;"
TEXTO_BLANCO_18 = "color: #FFFFFF; font-size: 18px;"
TEXTO_VERDE_18 = "color: #00FF00; font-size: 18px; font-weight: bold;"
TEXTO_AZUL_22 = "color: #00BFFF; font-size: 22px; font-weight: bold;"
TEXTO_DORADO_24 = "color: #FFD700; font-size: 24px; font-weight: bold;"

CALENDARIO_30 = "background-color: #222126; color: white; font-size: 30px; alternate-background-color: #131216;"
CALENDARIO_FUENTE_30 = "font-size: 30px;"
