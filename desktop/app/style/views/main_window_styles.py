# main_window_styles.py
ESTILO_MAIN_WINDOW = """
QWidget#main_container {
    background-color: #c8cbd0;
}

QWidget#sidebar {
    background-color: #1e1e24;
    border-right: 1px solid #3a3a4a;
}

QWidget#sidebar QPushButton {
    background-color: transparent;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 12px 15px;
    text-align: left;
    font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 14px;
    font-weight: bold;
}

QWidget#sidebar QPushButton:hover {
    background-color: #2a2a35;
    color: #e53935;
}

QWidget#sidebar QPushButton:pressed {
    background-color: #e53935;
    color: #ffffff;
}
"""