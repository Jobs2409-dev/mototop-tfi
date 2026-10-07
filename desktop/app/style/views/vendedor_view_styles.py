# desktop/app/style/views/vendedor_view_styles.py
ESTILO_VENDEDOR_VIEW = """
/* Barra Superior */
QPushButton#btn_nuevo_vendedor {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_nuevo_vendedor:hover {
    background-color: #0b7dda;
}

QPushButton#btn_refrescar_vendedor {
    background-color: #757575;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_refrescar_vendedor:hover {
    background-color: #616161;
}

/* Mensaje informativo */
QLabel#lbl_mensaje_info {
    color: #555555;
    font-size: 12px;
    font-style: italic;
    padding: 5px 2px;
}

/* Tabla de Vendedores */
QTableWidget#tabla_vendedores {
    background-color: #FFFFFF;
    alternate-background-color: #F9F9F9;
    gridline-color: #E0E0E0;
    border: 1px solid #D8D8D8;
    border-radius: 4px;
}

QHeaderView::section {
    background-color: #F5F5F5;
    color: #333333;
    padding: 6px;
    font-weight: bold;
    border: 1px solid #E0E0E0;
}

/* Botón Cambiar Estado en cada fila */
QPushButton#btn_cambiar_estado {
    background-color: #FF9800;
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 3px;
    font-weight: bold;
}
QPushButton#btn_cambiar_estado:hover {
    background-color: #e68900;
}
"""

# Constantes semánticas de color para celdas de estado
COLOR_ESTADO_ACTIVO = "#2E7D32"
COLOR_ESTADO_INACTIVO = "#C62828"