ESTILO_FORM_PEDIDO = """
/* Ventana principal */
QWidget#pedido_form_window {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2c3e50;
}

/* Etiquetas */
QLabel {
    font-size: 13px;
    font-weight: bold;
    color: #4a5568;
}

/* Campos de entrada, spinners, cuadros de texto y desplegables */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 13px;
    color: #2c3e50; /* Forzado de color oscuro para garantizar lectura */
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
    border: 1px solid #e53935; /* Foco Rojo Institucional */
}

/* Desplegable emergente de QComboBox (Lista de Clientes, Vendedores, Productos) */
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #2c3e50;
    selection-background-color: #e53935;
    selection-color: #ffffff;
    border: 1px solid #cbd5e1;
}

/* Tabla interna de ítems del pedido (si aplica) */
QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    gridline-color: #e2e8f0;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    font-size: 13px;
}

QTableWidget::item {
    padding: 4px 8px;
}

QHeaderView::section {
    background-color: #1e1e24;
    color: #ffffff;
    padding: 6px;
    font-weight: bold;
    border: none;
}

/* Botón secundario (+ Agregar Producto) */
QPushButton#btn_agregar {
    background-color: #1e1e24; /* Negro corporativo */
    color: #ffffff;
    font-weight: bold;
    font-size: 13px;
    border: none;
    border-radius: 5px;
    padding: 8px 15px;
}

QPushButton#btn_agregar:hover {
    background-color: #2d2d35;
}

/* Botón Principal (GUARDAR PEDIDO) */
QPushButton#btn_guardar_pedido {
    background-color: #e53935; /* Rojo Destacado */
    color: #ffffff;
    font-weight: bold;
    font-size: 14px;
    border: none;
    border-radius: 5px;
    padding: 12px;
}

QPushButton#btn_guardar_pedido:hover {
    background-color: #d32f2f;
}

QPushButton#btn_guardar_pedido:pressed {
    background-color: #b71c1c;
}

/* Botón Eliminar Fila de Ítem */
QPushButton#btn_eliminar_fila {
    background-color: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fca5a5;
    font-weight: bold;
    border-radius: 4px;
    padding: 5px;
}

QPushButton#btn_eliminar_fila:hover {
    background-color: #fecaca;
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