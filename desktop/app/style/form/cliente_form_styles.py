ESTILO_MODERNO = """
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        background-color: #f8f9fa;
        color: #333333;
    }
    QLineEdit, QComboBox {
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 6px 12px;
        background-color: #ffffff;
    }
    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #0d6efd;
        background-color: #fff;
    }
    QPushButton {
        background-color: #0d6efd;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #0b5ed7;
    }
    QPushButton:disabled {
        background-color: #6c757d;
    }
    QPushButton#btn_add_zona {
        background-color: #198754;
    }
    QPushButton#btn_add_zona:hover {
        background-color: #157347;
    }
    QTabWidget::pane {
        border: 1px solid #dee2e6;
        background: #ffffff;
        border-radius: 4px;
    }
    QTabBar::tab {
        background: #e9ecef;
        padding: 8px 16px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background: #ffffff;
        border-bottom: 2px solid #0d6efd;
        font-weight: bold;
    }
    QPushButton#btn_guardar {
    background-color: #6f42c1;  /* Morado principal */
    color: white;
    }

    QPushButton#btn_guardar:hover {
        background-color: #59359a;  /* Morado más oscuro al pasar el mouse */
    }

    QPushButton#btn_guardar:pressed {
        background-color: #492a80;  /* Morado aún más oscuro al hacer clic */
    }
"""
