# desktop/app/style/views/vendedor_view_styles.py

ESTILO_VENDEDOR_VIEW = """
/* Contenedor principal de la vista */
QWidget {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2c3e50;
}

/* ================================================================= */
/* BARRA SUPERIOR Y BOTONES DE ACCIÓN                                 */
/* ================================================================= */
QPushButton#btn_nuevo_vendedor {
    background-color: #FF6B00; /* Naranja identificativo */
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_nuevo_vendedor:hover {
    background-color: #e56000;
}
QPushButton#btn_nuevo_vendedor:pressed {
    background-color: #cc5500;
}

QPushButton#btn_refrescar_vendedor {
    background-color: #1e1e24;
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_refrescar_vendedor:hover {
    background-color: #33333d;
}

/* Mensaje informativo superior (sin fondo extra, totalmente integrado) */
QLabel#lbl_mensaje_info {
    background-color: transparent;
    color: #64748b;
    font-size: 12px;
    font-style: italic;
    padding: 0px 2px 5px 2px;
    border: none;
}

/* ================================================================= */
/* TABLA DE VENDEDORES                                               */
/* ================================================================= */
QTableWidget#tabla_vendedores {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    gridline-color: #e2e8f0;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 13px;
}

QTableWidget#tabla_vendedores::item {
    padding: 4px 8px;
}

QTableWidget#tabla_vendedores::item:selected {
    background-color: #FF6B00;
    color: #ffffff;
}

/* Cabecera de la Tabla */
QHeaderView::section {
    background-color: #1e1e24;
    color: #ffffff;
    padding: 8px;
    font-weight: bold;
    font-size: 13px;
    border: none;
    border-right: 1px solid #33333d;
}

/* Botón Cambiar Estado (Fix de tamaño y recorte) */
QPushButton#btn_cambiar_estado {
    background-color: #1e1e24;
    color: #ffffff;
    border: none;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
    max-height: 22px;
}

QPushButton#btn_cambiar_estado:hover {
    background-color: #FF6B00;
}

/* ================================================================= */
/* CONFIGURACIÓN MENSAJES DE CONFIRMACIÓN (QMessageBox)               */
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

# Colores vivos y bien legibles para la celda de Estado
COLOR_ESTADO_ACTIVO = "#16a34a"   # Verde brillante/vivo
COLOR_ESTADO_INACTIVO = "#dc2626" # Rojo brillante/vivo