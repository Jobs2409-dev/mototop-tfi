# desktop/app/style/views/cliente_view_style.py

ESTILO_CLIENTE_VIEW = """
/* Contenedor principal de la vista */
QWidget {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2c3e50;
}

/* ================================================================= */
/* BARRA SUPERIOR Y BOTONES DE ACCIÓN                                 */
/* ================================================================= */
QPushButton#btn_nuevo_cliente {
    background-color: #e53935; /* Rojo institucional del sistema */
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_nuevo_cliente:hover {
    background-color: #d32f2f;
}
QPushButton#btn_nuevo_cliente:pressed {
    background-color: #b71c1c;
}

QPushButton#btn_refrescar_cliente {
    background-color: #1e1e24; /* Gris/Negro secundario */
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#btn_refrescar_cliente:hover {
    background-color: #33333d;
}

/* ================================================================= */
/* TABLA DE CLIENTES                                                 */
/* ================================================================= */
QTableWidget#tabla_clientes {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    gridline-color: #e2e8f0;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 13px;
}

/* Se omite 'color' para permitir que setForeground() desde Python pinte sin bloqueos */
QTableWidget#tabla_clientes::item {
    padding: 4px 8px;
}

QTableWidget#tabla_clientes::item:selected {
    background-color: #e53935;
    color: #ffffff;
}

/* Cabecera de la Tabla */
QHeaderView::section {
    background-color: #1e1e24; /* Cabecera oscura elegante */
    color: #ffffff;
    padding: 8px;
    font-weight: bold;
    font-size: 13px;
    border: none;
    border-right: 1px solid #33333d;
}

/* ================================================================= */
/* BOTONES DE ACCIÓN DENTRO DE LA TABLA                              */
/* ================================================================= */
QPushButton#btn_accion_editar {
    background-color: #1e1e24;
    color: #ffffff;
    border: none;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
    max-height: 22px;
}
QPushButton#btn_accion_editar:hover {
    background-color: #33333d;
}

QPushButton#btn_accion_eliminar {
    background-color: #e53935;
    color: #ffffff;
    border: none;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11px;
    max-height: 22px;
}
QPushButton#btn_accion_eliminar:hover {
    background-color: #d32f2f;
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