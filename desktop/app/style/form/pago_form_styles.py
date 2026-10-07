QSS_STYLE = """
    QDialog {
        background-color: #1a1a1a;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #ffffff;
    }
    QLabel {
        font-weight: bold;
        color: #cccccc;
    }
    QLabel#lbl_factura {
        font-size: 14px;
        color: #ffffff;
        background-color: #262626;
        padding: 8px;
        border-left: 3px solid #dc3545;
        border-radius: 2px;
        margin-bottom: 5px;
    }
    QLineEdit, QComboBox, QDoubleSpinBox {
        background-color: #262626;
        border: 1px solid #333333;
        border-radius: 4px;
        padding: 6px;
        color: #ffffff;
        min-height: 20px;
    }
    QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
        border: 1px solid #dc3545;
    }
    QComboBox QAbstractItemView {
        background-color: #262626;
        color: #ffffff;
        selection-background-color: #dc3545;
    }
    QPushButton {
        background-color: #dc3545;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
        margin-top: 10px;
    }
    QPushButton:hover {
        background-color: #bd2130;
    }
    QPushButton:pressed {
        background-color: #b02a37;
    }
"""