# desktop/app/style/views/factura_view_style.py
ESTILO_VIEW_FACTURA = """
QWidget#main_factura_view {
    background-color: #f5f6f8;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QWidget#scroll_container {
    background-color: transparent;
}

QPushButton#btn_recargar {
    background-color: #757575;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_recargar:hover {
    background-color: #616161;
}

QWidget#contenedor_factura_card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
}

QLabel#title_factura {
    font-size: 15px;
    font-weight: bold;
    color: #1e1e24;
}

QLabel#meta_info_factura {
    font-size: 12px;
    color: #4a5568;
}

QLabel#cliente_factura {
    font-size: 13px;
    font-weight: 600;
    color: #2d3748;
}

QLabel#total_factura {
    font-size: 16px;
    font-weight: bold;
    color: #15803d;
}

QLabel#badge_pagada {
    background-color: #dcfce7;
    color: #15803d;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
}

QLabel#badge_pendiente {
    background-color: #fef3c7;
    color: #d97706;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
}

QPushButton#btn_pagos {
    background-color: #1e1e24;
    color: white;
    border: none;
    padding: 6px 14px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 12px;
}
QPushButton#btn_pagos:hover {
    background-color: #2d2d35;
}
"""