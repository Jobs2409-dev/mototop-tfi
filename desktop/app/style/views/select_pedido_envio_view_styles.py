# desktop/app/style/views/select_pedido_envio_view_styles.py
QSS_STYLE = """
    QWidget#SelectPedidoEnvioView {
        background-color: #ffffff;
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
        background-color: #f8f9fa;
        color: #495057;
        padding: 8px;
        font-weight: bold;
        border: none;
        border-bottom: 2px solid #dee2e6;
    }
    QTableWidget::item {
        padding: 6px;
    }
    QTableWidget::item:selected {
        background-color: #f8d7da;
        color: #b02a37;
    }
    QPushButton#btn_seleccionar {
        background-color: #dc3545;
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
        background-color: #bd2130;
    }
    QPushButton#btn_seleccionar:pressed {
        background-color: #b02a37;
    }
"""