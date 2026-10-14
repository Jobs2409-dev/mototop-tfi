QSS_STYLE = """
/* Ventana/Contenedor principal del formulario de envíos */
QDialog#EnvioForm, QWidget#EnvioForm {
    background-color: #f8f9fa;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #212529;
}

/* Etiquetas generales */
QLabel {
    font-size: 13px;
    font-weight: bold;
    color: #343a40;
}

/* Checkbox */
QCheckBox {
    font-size: 13px;
    color: #343a40;
}

/* Campos de entrada, desplegables y selector de fecha/hora */
QLineEdit, QComboBox, QDateTimeEdit {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 5px;
    padding: 6px 10px;
    color: #212529;
    font-size: 13px;
}

QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus {
    border: 1px solid #e53935;
    background-color: #ffffff;
}

/* Items dentro de Combobox */
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #212529;
    selection-background-color: #e53935;
    selection-color: #ffffff;
    border: 1px solid #ced4da;
}

/* Botón secundario para Buscar Pedido */
QPushButton {
    background-color: #1e1e24;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 6px 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #33333d;
}

/* Botón de Guardar / Registrar Envío */
QPushButton#btn_save {
    background-color: #e53935;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 10px;
    font-size: 14px;
    font-weight: bold;
    margin-top: 10px;
}

QPushButton#btn_save:hover {
    background-color: #d32f2f;
}

QPushButton#btn_save:pressed {
    background-color: #b71c1c;
}

/* Diálogos de mensaje */
QMessageBox {
    background-color: #ffffff;
}

QMessageBox QLabel {
    color: #212529 !important;
    font-weight: normal;
}
"""