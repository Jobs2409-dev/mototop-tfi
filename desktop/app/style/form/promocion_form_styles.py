QSS_STYLE = """
/* Ventana principal y fondo general */
QWidget {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #2c3e50;
}

/* Etiquetas */
QLabel {
    font-weight: bold;
    color: #4a5568;
}

QLabel#section_title {
    font-size: 18px;
    font-weight: bold;
    color: #1e1e24;
    border-bottom: 2px solid #e53935;
    padding-bottom: 5px;
}

/* Campos de texto, combos, fechas y números */
QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QSpinBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 8px 12px;
    font-size: 13px;
    color: #2c3e50;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {
    border: 1px solid #e53935;
}

/* Desplegable de QComboBox */
QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #2c3e50;
    selection-background-color: #e53935;
    selection-color: #ffffff;
}

/* Botón Principal (Guardar / Crear Promoción) */
QPushButton {
    background-color: #e53935;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 12px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #d32f2f;
}

QPushButton:pressed {
    background-color: #b71c1c;
}

/* Botones Secundarios (si usas objectName="secondary_button") */
QPushButton#secondary_button {
    background-color: #1e1e24;
    color: #ffffff;
    font-size: 13px;
    padding: 8px 15px;
}

QPushButton#secondary_button:hover {
    background-color: #2d2d35;
}

/* ================================================================= */
/* CONFIGURACIÓN PARA EL MENSAJE DE CONFIRMACIÓN (QMessageBox)        */
/* ================================================================= */
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