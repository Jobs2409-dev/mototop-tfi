ESTILO_VENDEDOR_FORM = """
QWidget#vendedor_form_window {
    background-color: #F5F5F5;
    font-size: 13px;
    color: #333333;
}

QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #D8D8D8;
    border-radius: 6px;
    margin-top: 15px;
    font-weight: bold;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 15px;
    padding: 0 5px;
    color: #2196F3;
}

QLineEdit, QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    padding: 6px;
    min-height: 20px;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #2196F3;
}

QPushButton#btn_add_zona {
    background-color: #2196F3;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 4px;
    padding: 6px;
}
QPushButton#btn_add_zona:hover {
    background-color: #0b7dda;
}
QPushButton#btn_add_zona:disabled {
    background-color: #BDBDBD;
}

QPushButton#btn_save {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    font-size: 14px;
    border: none;
    border-radius: 4px;
    padding: 10px;
    min-height: 25px;
}
QPushButton#btn_save:hover {
    background-color: #43A047;
}
"""