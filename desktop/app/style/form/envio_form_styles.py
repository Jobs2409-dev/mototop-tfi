QSS_STYLE = """
    QWidget#EnvioForm {
        background-color: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #1a1a1a;
    }
    QLabel {
        font-weight: bold;
        color: #495057;
    }
    QLabel#lbl_pedido_header {
        font-size: 15px;
        font-weight: bold;
        color: #ffffff;
        background-color: #212529;
        padding: 10px;
        border-left: 4px solid #dc3545;
        border-radius: 4px;
        margin-bottom: 5px;
    }
    QLineEdit, QComboBox, QDateTimeEdit {
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 6px;
        color: #212529;
        min-height: 22px;
    }
    QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus {
        border: 1px solid #dc3545;
        background-color: #ffffff;
    }
    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #212529;
        selection-background-color: #dc3545;
        selection-color: white;
    }
    QPushButton#btn_save {
        background-color: #dc3545;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 12px;
        font-size: 14px;
        font-weight: bold;
        margin-top: 15px;
    }
    QPushButton#btn_save:hover {
        background-color: #bd2130;
    }
    QPushButton#btn_save:pressed {
        background-color: #b02a37;
    }
"""