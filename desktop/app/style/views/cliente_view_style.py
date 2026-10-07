# desktop/app/style/views/cliente_view_style.py
ESTILO_CLIENTE_VIEW = """
/* Barra Superior */
QPushButton#btn_nuevo_cliente {
    background-color: #673AB7;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_nuevo_cliente:hover {
    background-color: #5E35B1;
}

QPushButton#btn_refrescar_cliente {
    background-color: #757575;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_refrescar_cliente:hover {
    background-color: #616161;
}

/* Tabla de Clientes */
QTableWidget#tabla_clientes {
    background-color: #FFFFFF;
    alternate-background-color: #F9F9F9;
    gridline-color: #E0E0E0;
    border: 1px solid #D8D8D8;
    border-radius: 4px;
    selection-background-color: #EDE7F6;
    selection-color: #311B92;
}

QHeaderView::section {
    background-color: #F5F5F5;
    color: #333333;
    padding: 6px;
    font-weight: bold;
    border: 1px solid #E0E0E0;
}

/* Botones de Acción dentro de la Tabla */
QPushButton#btn_accion_editar {
    background-color: #673AB7;
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 3px;
    font-weight: bold;
}
QPushButton#btn_accion_editar:hover {
    background-color: #5E35B1;
}

QPushButton#btn_accion_eliminar {
    background-color: #E53935;
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 3px;
    font-weight: bold;
}
QPushButton#btn_accion_eliminar:hover {
    background-color: #D32F2F;
}
"""