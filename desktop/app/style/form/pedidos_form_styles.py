ESTILO_FORM_PEDIDO = """
QWidget#pedido_form_window {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QLabel {
    font-size: 13px;
    font-weight: bold;
    color: #4a5568;
}

QComboBox, QSpinBox, QTextEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 13px;
}

QComboBox:focus, QSpinBox:focus, QTextEdit:focus {
    border: 1px solid #e53935; /* Foco Rojo Administrativo */
}

QPushButton#btn_agregar {
    background-color: #1e1e24; /* Negro corporativo */
    color: white;
    font-weight: bold;
    border-radius: 5px;
    padding: 8px 15px;
}
QPushButton#btn_agregar:hover {
    background-color: #2d2d35;
}

QPushButton#btn_guardar_pedido {
    background-color: #e53935; /* Rojo Destacado */
    color: white;
    font-weight: bold;
    font-size: 14px;
    border-radius: 5px;
    padding: 12px;
}
QPushButton#btn_guardar_pedido:hover {
    background-color: #d32f2f;
}

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
"""