ESTILO_PRODUCTO_FORM = """
QWidget#producto_form_window {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2c3e50;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: #f5f6f8;
}

QWidget#form_content_widget {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2c3e50;
}

QWidget#producto_form_window {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2c3e50;
}

QLabel {
    font-size: 13px;
    font-weight: bold;
    color: #4a5568;
}

QLabel#section_title {
    font-size: 18px;
    font-weight: bold;
    color: #1e1e24;
    border-bottom: 2px solid #e53935;
    padding-bottom: 5px;
}

QLabel#sub_title {
    font-size: 13px;
    color: #1e1e24;
    font-weight: bold;
}

QLabel#image_status {
    font-size: 12px;
    color: #64748b;
    font-style: italic;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 8px 12px;
    font-size: 13px;
    color: #2c3e50
}

QLineEdit:focus {
    border: 1px solid #e53935;
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 5px;
    color: #2c3e50;
}

QListWidget::item {
    padding: 6px;
    border-bottom: 1px solid #f1f5f9;
    color: #2c3e50;
}

QListWidget::item:selected {
    background-color: #e53935;
    color: #ffffff;
    border-radius: 3px;
}

/* Paneles Ocultables */
QWidget#sub_panel {
    background-color: #eaf0f6;
    border: 1px solid #d1d5db;
    border-radius: 6px;
}

/* Botones */
QPushButton {
    font-weight: bold;
    font-size: 13px;
    border-radius: 5px;
    padding: 8px 15px;
    border: none;
}

QPushButton#toggle_button {
    background-color: #e2e8f0;
    color: #475569;
    border: 1px solid #cbd5e1;
}
QPushButton#toggle_button:checked {
    background-color: #475569;
    color: #ffffff;
}

QPushButton#secondary_button {
    background-color: #1e1e24;
    color: #ffffff;
}
QPushButton#secondary_button:hover {
    background-color: #2d2d35;
}

QPushButton#main_save_button {
    background-color: #e53935;
    color: #ffffff;
    font-size: 14px;
    padding: 12px;
}
QPushButton#main_save_button:hover {
    background-color: #d32f2f;
}

QPushButton#action_green {
    background-color: #2ecc71;
    color: #ffffff;
    font-size: 12px;
    padding: 6px;
}
QPushButton#action_green:hover {
    background-color: #27ae60;
}

QPushButton#action_red {
    background-color: #e74c3c;
    color: #ffffff;
    font-size: 12px;
    padding: 6px;
}
QPushButton#action_red:hover {
    background-color: #c0392b;
}

QMessageBox {
    background-color: #ffffff; /* Fondo blanco */
    border: 1px solid #cbd5e1;
}

/* Fuerza el texto a color oscuro legible */
QMessageBox QLabel {
    color: #2c3e50 !important;
    font-weight: normal;
    font-size: 13px;
    background-color: transparent;
}

/* Estilo claro y elegante para los botones de la confirmación */
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