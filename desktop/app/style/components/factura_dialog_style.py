# desktop/app/style/components/factura_dialog_style.py
ESTILO_DIALOG_FACTURA = """
QDialog {
    background-color: #f5f6f8;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QLabel {
    color: #1e1e24;
    font-size: 13px;
}

QLabel#title_dialog {
    font-size: 16px;
    font-weight: bold;
    color: #1e1e24;
    border-bottom: 2px solid #e53935; /* Subrayado Rojo Admin */
    padding-bottom: 4px;
}

QLabel#total_dialog {
    font-size: 14px;
    font-weight: bold;
    color: #1e1e24;
}

QTextEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace; /* Tipografía limpia para tickets */
    font-size: 12px;
    color: #2d3748;
}

QPushButton#btn_cerrar_dialog {
    background-color: #1e1e24; /* Negro corporativo */
    color: white;
    font-weight: bold;
    font-size: 13px;
    border: none;
    border-radius: 4px;
    padding: 8px 20px;
}
QPushButton#btn_cerrar_dialog:hover {
    background-color: #2d2d35;
}
"""