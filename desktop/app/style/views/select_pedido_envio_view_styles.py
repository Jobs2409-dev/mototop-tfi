QSS_STYLE = """
    QDialog, QWidget#SelectPedidoEnvioView {
        background-color: #f8f9fa;
    }
    QLabel {
        color: #212529;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QTableWidget {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        gridline-color: #f1f3f5;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #212529;
    }
    QHeaderView::section {
        background-color: #1e1e24;
        color: #ffffff;
        padding: 8px;
        font-weight: bold;
        border: none;
    }
    QTableWidget::item {
        padding: 6px;
        color: #212529;
    }
    QTableWidget::item:selected {
        background-color: #e53935;
        color: #ffffff;
    }
    QPushButton#btn_seleccionar {
        background-color: #e53935;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
        font-weight: bold;
        margin-top: 10px;
    }
    QPushButton#btn_seleccionar:hover {
        background-color: #d32f2f;
    }
    QPushButton#btn_seleccionar:pressed {
        background-color: #b71c1c;
    }
"""