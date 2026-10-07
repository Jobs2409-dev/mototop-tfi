# desktop/app/style/views/compra_view_styles.py
QSS_STYLE = """
    QWidget#CompraView {
        background-color: #ffffff;
    }
    QLabel#lbl_titulo {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 20px;
        font-weight: bold;
        color: #1a1a1a;
    }
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    QWidget#scroll_container {
        background-color: transparent;
    }
    QPushButton#btn_new {
        background-color: #dc3545;
        color: white;
        border: none;
        padding: 10px 18px;
        border-radius: 4px;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton#btn_new:hover {
        background-color: #bd2130;
    }
    QPushButton#btn_new:pressed {
        background-color: #b02a37;
    }
"""