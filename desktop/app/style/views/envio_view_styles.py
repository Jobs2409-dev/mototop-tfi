QSS_STYLE = """
/* Contenedor/Fondo principal de la vista de envíos */
QWidget#EnvioView {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2c3e50;
}

/* Botones secundarios generales */
QPushButton {
    background-color: #1e1e24;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 8px 16px;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #33333d;
}

/* Botón Principal */
QPushButton#btn_crear {
    background-color: #e53935;
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton#btn_crear:hover {
    background-color: #d32f2f;
}

QPushButton#btn_crear:pressed {
    background-color: #b71c1c;
}

/* Tabla de Envíos */
QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    gridline-color: #e2e8f0;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #212529;
}

QTableWidget::item {
    padding: 4px 8px;
    color: #212529;
}

QTableWidget::item:selected {
    background-color: #e53935;
    color: #ffffff;
}

/* Cabecera de la Tabla */
QHeaderView::section {
    background-color: #1e1e24;
    color: #ffffff;
    padding: 8px;
    font-weight: bold;
    font-size: 13px;
    border: none;
    border-right: 1px solid #33333d;
}

QMessageBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
}

QMessageBox QLabel {
    color: #2c3e50 !important;
    font-weight: normal;
    font-size: 13px;
    background-color: transparent;
}

QMessageBox QPushButton {
    background-color: #f1f5f9;
    color: #2c3e50;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    font-weight: bold;
    padding: 6px 15px;
    min-width: 70px;
}

QMessageBox QPushButton:hover {
    background-color: #e2e8f0;
}
"""