# desktop/app/style/components/pedido_card_styles.py
ESTILO_CARD_PEDIDO = """
QWidget#contenedor_card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
}

QLabel {
    color: #1e1e24;
    font-size: 13px;
}

QLabel#id_pedido {
    color: #1e1e24;
    font-size: 14px;
    font-weight: bold;
}

QLabel#cliente_pedido {
    color: #2d3748;
    font-weight: 600;
}

QLabel#meta_info {
    color: #718096;
    font-size: 12px;
}

QLabel#total_pedido {
    color: #1e1e24;
    font-size: 14px;
    font-weight: bold;
}

/* Badges de Estado */
QLabel#badge_pendiente {
    background-color: #fef3c7;
    color: #d97706;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
}

QLabel#badge_confirmado {
    background-color: #dcfce7;
    color: #15803d;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
}

QLabel#badge_cancelado {
    background-color: #fee2e2;
    color: #b91c1c;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
}

/* Botones de acción dentro de la card */
QWidget#contenedor_card QPushButton {
    font-weight: bold;
    font-size: 12px;
    border-radius: 4px;
    padding: 6px 14px;
    color: white;
}

QWidget#contenedor_card QPushButton#btn_confirmar {
    background-color: #15803d;
}
QWidget#contenedor_card QPushButton#btn_confirmar:hover {
    background-color: #166534;
}

QWidget#contenedor_card QPushButton#btn_cancelar {
    background-color: #e53935;  /* Rojo Admin */
}
QWidget#contenedor_card QPushButton#btn_cancelar:hover {
    background-color: #b71c1c;
}

QWidget#contenedor_card QPushButton#btn_factura {
    background-color: #1e1e24;  /* Negro corporativo */
}
QWidget#contenedor_card QPushButton#btn_factura:hover {
    background-color: #2d2d35;
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