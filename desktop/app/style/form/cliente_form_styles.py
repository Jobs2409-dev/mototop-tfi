ESTILO_MODERNO = """
/* Contenedor principal y fondo */
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    background-color: #f5f6f8;
    color: #2c3e50;
}

/* Etiquetas */
QLabel {
    font-weight: bold;
    color: #4a5568;
}

/* Campos de texto y desplegables */
QLineEdit, QComboBox {
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 8px 12px;
    background-color: #ffffff;
    color: #2c3e50;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #e53935; /* Foco institucional en rojo */
    background-color: #ffffff;
}

/* Desplegable de QComboBox */
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #2c3e50;
    selection-background-color: #e53935;
    selection-color: #ffffff;
}

/* Estilo general para botones */
QPushButton {
    background-color: #1e1e24;
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #33333d;
}

QPushButton:disabled {
    background-color: #cbd5e1;
    color: #94a3b8;
}

/* Botón secundario para agregar zonas */
QPushButton#btn_add_zona {
    background-color: #1e1e24;
    color: #ffffff;
}

QPushButton#btn_add_zona:hover {
    background-color: #33333d;
}

/* Botón principal de Guardar */
QPushButton#btn_guardar {
    background-color: #e53935; /* Rojo principal del sistema */
    color: #ffffff;
    font-size: 14px;
    padding: 12px;
}

QPushButton#btn_guardar:hover {
    background-color: #d32f2f;
}

QPushButton#btn_guardar:pressed {
    background-color: #b71c1c;
}

/* Pestañas (QTabWidget) */
QTabWidget::pane {
    border: 1px solid #cbd5e1;
    background: #ffffff;
    border-radius: 6px;
}

QTabBar::tab {
    background: #e2e8f0;
    color: #475569;
    padding: 8px 16px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 2px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background: #ffffff;
    color: #1e1e24;
    border-bottom: 3px solid #e53935; /* Indicador rojo en la pestaña activa */
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