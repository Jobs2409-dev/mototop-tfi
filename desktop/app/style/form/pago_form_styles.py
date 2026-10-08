QSS_STYLE = """
    QWidget {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #212529;
    }
    
    #lbl_factura {
        font-size: 14px;
        font-weight: bold;
        color: #d93025;
        background-color: #fce8e6;
        border: 1px solid #f8c2c0;
        border-left: 5px solid #ea4335;
        border-radius: 6px;
        padding: 10px 14px;
    }
    
    QLabel {
        font-weight: 600;
        color: #3c4043;
    }
    
    QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 6px;
        padding: 8px 10px;
        font-size: 13px;
        color: #212529;
    }
    
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
        border: 2px solid #ea4335;
        background-color: #ffffff;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left-width: 0px;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
    }
    
    QPushButton {
        background-color: #ea4335;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 10px 18px;
        font-size: 14px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #d93025;
    }
    
    QPushButton:pressed {
        background-color: #b3261e;
    }
    
    QPushButton:disabled {
        background-color: #f1f3f4;
        color: #bdc1c6;
    }
"""