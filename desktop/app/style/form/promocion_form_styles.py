QSS_STYLE = """
    QWidget {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #333333;
    }
    QLabel {
        font-weight: bold;
        color: #495057;
    }
    QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 6px;
        min-height: 20px;
    }
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
        border: 1px solid #0d6efd;
    }
    QPushButton {
        background-color: #0d6efd;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #0b5ed7;
    }
    QPushButton:pressed {
        background-color: #0a58ca;
    }
"""