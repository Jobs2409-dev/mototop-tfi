# desktop/app/style/views/informe_view_style.py
QSS_STYLE = """
    QWidget#InformeView {
        background-color: #ffffff;
    }
    QLabel {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #495057;
    }
    QLabel#lbl_seccion {
        font-size: 15px;
        font-weight: bold;
        color: #1a1a1a;
        margin-top: 15px;
        margin-bottom: 5px;
    }
    QDateEdit {
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 6px;
        color: #212529;
        min-height: 20px;
        font-weight: bold;
    }
    QDateEdit:focus {
        border: 1px solid #dc3545;
        background-color: #ffffff;
    }
    QPushButton#btn_refresh {
        background-color: #dc3545;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton#btn_refresh:hover {
        background-color: #bd2130;
    }
    QPushButton#btn_refresh:pressed {
        background-color: #b02a37;
    }
    QGroupBox#metric_card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
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