ESTILO_PRODUCTO_VIEW = """
/* Barra superior */
QPushButton#btn_nuevo_producto {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_nuevo_producto:hover {
    background-color: #0b7dda;
}

/* Botones secundarios (Paginación y Recargar) */
QPushButton.btn_secondary_action {
    background-color: #757575;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton.btn_secondary_action:hover {
    background-color: #616161;
}

/* Indicador de página */
QLabel#lbl_numero_pagina {
    font-size: 13px;
    font-weight: bold;
    color: #495057;
    padding-left: 8px;
}

/* Área de scroll de productos */
QScrollArea#scroll_productos {
    border: none;
    background-color: transparent;
}

/* Restricción para impedir desbordes horizontales */
QScrollArea#scroll_productos > QWidget > QWidget {
    background-color: transparent;
}

QWidget#standard_card, QWidget#active_promo_card {
    min-width: 0px;
}
"""