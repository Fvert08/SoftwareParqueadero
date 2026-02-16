MESSAGEBOX_STYLESHEET = """
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


def apply_global_messagebox_style(app):
    existing_stylesheet = app.styleSheet() or ""

    if MESSAGEBOX_STYLESHEET.strip() in existing_stylesheet:
        return

    app.setStyleSheet(f"{existing_stylesheet}\n{MESSAGEBOX_STYLESHEET}".strip())
