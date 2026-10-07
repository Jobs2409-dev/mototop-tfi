# desktop/app/style/views/envio_view_styles.py
QSS_STYLE = """
    QWidget#EnvioView {
        background-color: #ffffff;
    }
    QPushButton {
        background-color: #f8f9fa;
        color: #212529;
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 8px 14px;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #e9ecef;
        border-color: #adb5bd;
    }
    QPushButton#btn_crear {
        background-color: #dc3545;
        color: white;
        border: none;
    }
    QPushButton#btn_crear:hover {
        background-color: #bd2130;
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
"""
