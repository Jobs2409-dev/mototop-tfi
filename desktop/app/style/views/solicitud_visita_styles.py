# desktop/app/style/views/solicitud_visita_styles.py

ESTILO_SOLICITUD_VISITA = """
/* Botón Acción Principal (Recargar) */
QPushButton#btn_recargar {
    background-color: #212529;
    color: #ffffff;
    font-size: 13px;
    font-weight: bold;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
}

QPushButton#btn_recargar:hover {
    background-color: #343a40;
}

QPushButton#btn_recargar:pressed {
    background-color: #121416;
}

/* Tabla General */
QTableWidget {
    background-color: #ffffff;
    gridline-color: #e0e0e0;
    border: 1px solid #dcdcdc;
    font-size: 12px;
    color: #212529;
    selection-background-color: #e3f2fd;
    selection-color: #000000;
}

/* Encabezados de la Tabla */
QHeaderView::section {
    background-color: #212529;
    color: #ffffff;
    font-weight: bold;
    font-size: 12px;
    padding: 8px 4px;
    border: none;
    border-right: 1px solid #343a40;
    text-align: center;
}

/* Números de Fila (Vertical Header) */
QHeaderView::section:vertical {
    background-color: #212529;
    color: #ffffff;
    font-weight: bold;
    font-size: 12px;
    text-align: center;
    border-bottom: 1px solid #343a40;
}

/* Desplegable de Estado en Fila (Estilo base) */
QComboBox {
    background-color: #f8f9fa;
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
    color: #212529; /* Texto visible en el combo cerrado */
}

QComboBox:hover {
    border-color: #e53935;
}

QComboBox::drop-down {
    border: none;
}

/* ==========================================================================
   SOLUCIÓN AL TEXTO INVISIBLE (Desplegables)
   Forzar texto oscuro e interfaz de selección corporativa
   ========================================================================== */

/* Control de la lista desplegable entera */
QComboBox QAbstractItemView {
    background-color: #ffffff !important; 
    border: 1px solid #ced4da;
    border-radius: 4px;
    color: #212529 !important; /* Texto oscuro e impositivo */
    selection-background-color: #e53935 !important; /* Fondo rojo en hover */
    selection-color: #ffffff !important; /* Texto blanco en hover */
    padding: 4px;
    outline: 0px;
}

/* Elementos individuales dentro del desplegable */
QComboBox QAbstractItemView::item {
    padding: 6px 12px;
    background-color: #ffffff;
    color: #212529 !important; /* Asegurar el texto en gris oscuro */
}

/* Estilo cuando el usuario pasa el mouse por encima (hover) */
QComboBox QAbstractItemView::item:hover {
    background-color: #e53935 !important;
    color: #ffffff !important;
}

/* Estilo del elemento seleccionado/activo */
QComboBox QAbstractItemView::item:selected {
    background-color: #e53935 !important;
    color: #ffffff !important;
}
"""