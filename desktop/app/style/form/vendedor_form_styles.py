ESTILO_VENDEDOR_FORM = """
/* Ventana principal */
QWidget#vendedor_form_window {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #2c3e50;
}

/* Grupos de secciones (Tarjetas blancas contenedor) */
QGroupBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    margin-top: 18px;
    padding: 15px 12px 12px 12px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 8px;
    color: #FF6B00; /* Naranja identificativo para Vendedores */
    font-size: 13px;
    background-color: #f5f6f8; /* Para que corte limpio la línea del borde */
}

/* Etiquetas generales */
QLabel {
    font-weight: bold;
    color: #4a5568;
}

/* Campos de entrada e Insumos */
QLineEdit, QComboBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 8px 12px;
    font-size: 13px;
    color: #2c3e50;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #FF6B00; /* Enfoque en tono naranja */
}

/* Desplegable de QComboBox */
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #2c3e50;
    selection-background-color: #FF6B00;
    selection-color: #ffffff;
}

/* Botón secundario (+ Zona) */
QPushButton#btn_add_zona {
    background-color: #1e1e24;
    color: #ffffff;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    padding: 8px 14px;
}

QPushButton#btn_add_zona:hover {
    background-color: #33333d;
}

QPushButton#btn_add_zona:disabled {
    background-color: #cbd5e1;
    color: #94a3b8;
}

/* Botón Principal de Guardar (Naranja del módulo) */
QPushButton#btn_save {
    background-color: #FF6B00;
    color: #ffffff;
    font-weight: bold;
    font-size: 14px;
    border: none;
    border-radius: 5px;
    padding: 12px;
    min-height: 22px;
}

QPushButton#btn_save:hover {
    background-color: #e56000;
}

QPushButton#btn_save:pressed {
    background-color: #cc5500;
}

/* ================================================================= */
/* CONFIGURACIÓN EXCLUSIVA PARA EL MENSAJE DE CONFIRMACIÓN (QMessageBox) */
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