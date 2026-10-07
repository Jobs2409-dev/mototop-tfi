# desktop/app/style/views/factura_view_style.py
ESTILO_VIEW_FACTURA = """
QWidget#main_factura_view {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QScrollArea {
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    background-color: #ffffff;
}

QWidget#scroll_container {
    background-color: #ffffff;
}

/* Botón superior de Recargar (Negro Corporativo) */
QPushButton#btn_recargar {
    background-color: #1e1e24;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_recargar:hover {
    background-color: #2d2d35;
}

/* Tarjeta contenedora física de la Factura */
QWidget#contenedor_factura_card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
}

QLabel {
    color: #1e1e24;
    font-size: 13px;
}

QLabel#title_factura {
    font-size: 14px;
    font-weight: bold;
    color: #1e1e24;
}

QLabel#total_factura {
    font-size: 14px;
    font-weight: bold;
    color: #1e1e24;
}

QLabel#meta_info_factura {
    color: #718096;
    font-size: 12px;
}

/* Badges Condicionales de Pago */
QLabel#badge_pagada {
    background-color: #dcfce7;
    color: #15803d;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
}

QLabel#badge_pendiente {
    background-color: #fee2e2;
    color: #b91c1c;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
}

/* Botón interno de la Tarjeta (Rojo Administrativo) */
QWidget#contenedor_factura_card QPushButton {
    background-color: #e53935;
    color: white;
    font-weight: bold;
    font-size: 12px;
    border: none;
    border-radius: 4px;
    padding: 6px 14px;
}
QWidget#contenedor_factura_card QPushButton:hover {
    background-color: #d32f2f;
}
"""
